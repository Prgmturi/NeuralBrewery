"""The plant agent: from an alarm to a diagnosis, on datapizza.

It starts from the alarms of the controller and the judgements of the
watcher, reads the plant with its tools, and hands in a diagnosis with
submit_diagnosis. What datapizza leaves to the caller with Claude, found in
the trial of M5 (docs/decisioni.md, "datapizza con Claude"):

- tool_choice is always "auto": a forced tool is a 400 on the current models;
- the arguments of every call (tokens, effort...) come from the adapter;
- a step with no text and no tool, as a refusal is, stops the loop: datapizza
  would ask the model again until max_steps;
- datapizza prints every step on the console: here they go to the logs.

Every step is traced with datapizza's ContextTracing, in process: the run
carries the steps, with stop reasons and tokens, for the evals and the audit.
"""

from collections.abc import Iterable, Mapping
from typing import Any

from datapizza.agents import Agent, AgentHooks, StepContext, StepResult
from datapizza.agents.logger import AgentLogger
from datapizza.core.clients import Client
from datapizza.tracing import ContextTracing

from neuralbrewery.core.logging import get_logger
from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.readonly import ReadOnlyPlant
from neuralbrewery.core.plant.schemas import PlantState, ProgramStatus, WatcherAlarm
from neuralbrewery.features.agents.diagnosis import DiagnosisRun, Outcome, Step
from neuralbrewery.features.agents.tools import (
    Submission,
    reading_tools,
    submit_tool,
)

logger = get_logger(__name__)

NAME = "plant_agent"
MAX_STEPS = 12

SYSTEM_PROMPT = """\
Sei l'agente impianto di un birrificio pilota da 20 L. Quando il controllore o \
il sorvegliante danno un allarme, trovi la causa e proponi che cosa fare. Leggi \
l'impianto solo con i tool. Non puoi comandarlo: un comando che indichi è solo \
una proposta, che il birraio approva o no.

L'impianto
- Recipienti: HLT (acqua calda, 40 L, resistenza R1); MASH (tino, 30 L, \
resistenza R2, agitatore M1 con inverter); BOIL (bollitore, 40 L, resistenza R3); \
FERM (fermentatore, 26,5 L, fascia R4, serpentina a glicole aperta dalla valvola EV9).
- Temperature: sonde PT100 con trasmettitore 4-20 mA, TT1 (HLT), TT2 (MASH), \
TT3 (BOIL), TT5a e TT5b (FERM: TT5a regola, TT5b è di confronto e di riserva). \
Livelli: LT1-LT4. Nel fermentatore, dopo l'inoculo, l'iSpindel DT1 manda densità \
e temperatura (DT1.temperature) ogni 15 minuti.
- Percorsi: hlt_to_mash e hlt_to_boil con la pompa P1; mash_recirc, mash_to_boil \
e boil_to_ferm con la pompa P2. Il controllore apre e chiude le valvole (EV2a-EV7), \
che hanno i fine corsa. Pompe e resistenze non danno ritorno: si vedono solo \
dagli effetti.
- Un travaso si ferma da solo alla quantità chiesta, e conta i litri sul livello \
della sorgente.
- Il contattore K1, cablato, toglie corrente a tutte le resistenze se una \
temperatura vera supera la soglia del suo termostato: il controllore vede solo \
"K1 aperto".
- Il controllore non riparte mai da solo: ciò che un interlock ha fermato resta \
fermo, con il suo allarme, fino a reset o a un nuovo comando sulla stessa cosa. \
Il programma della cotta, in 15 passi, preme gli stessi pulsanti del birraio, e \
quando qualcosa si blocca va in pausa.

Come ragionare
- Il controllore conosce solo i segnali dei dispositivi: uno strumento guasto lo \
inganna, e lui agisce su ciò che crede. Distingui un guasto di misura (lo \
strumento mente, l'impianto è sano) da un guasto di processo (l'impianto è \
guasto, le misure sono giuste).
- Confronta strumenti indipendenti che misurano la stessa cosa; guarda lo storico \
e gli eventi: quando è cominciato, che cosa è cambiato.
- Se più cause spiegano gli stessi dati e i tool non bastano a distinguerle, non \
scegliere a caso: confirmed è false, e checks dice le verifiche a mano che le \
distinguono.
- Il tempo è simulato: sim_time_s conta i secondi dall'inizio della simulazione.

La risposta
- Chiudi sempre chiamando submit_diagnosis, una volta sola. Non rispondere a testo.
- component è la sigla del componente guasto (per esempio TT5a, P1, M1), o il \
percorso se non si può dire di più.
- command è un pulsante del pannello, o nessuno se prima servono verifiche. \
Proponi il più prudente: non far ripartire ciò che si è fermato finché la causa \
non è chiara.
- explanation e checks sono per il birraio: in italiano, brevi e concreti.
"""


def task(state: PlantState, judged: Iterable[WatcherAlarm]) -> str:
    """The first message: what is wrong now, as controller and watcher say."""
    lines = [f"Tempo simulato: {_clock(state.sim_time_s)}."]
    program = state.program
    if program.status is not ProgramStatus.IDLE:
        lines.append(
            f"Programma: {program.status}, passo {program.step} ({program.step_name})"
            + (f", motivo: {program.reason}" if program.reason else "")
            + "."
        )
    alarms = [
        f"- {alarm.code} su {alarm.tag}, da {_clock(alarm.since_s)}: {alarm.text}"
        for alarm in state.alarms
    ]
    lines += (
        ["Allarmi del controllore:", *alarms]
        if alarms
        else ["Nessun allarme del controllore."]
    )
    judgements = [
        f"- {alarm.code} su {alarm.tag}, da {_clock(alarm.since_s)}: {alarm.text}"
        for alarm in judged
    ]
    lines += (
        ["Giudizi del sorvegliante:", *judgements]
        if judgements
        else ["Nessun giudizio del sorvegliante."]
    )
    lines.append(
        "Trova la causa con i tool, poi consegna la diagnosi con submit_diagnosis."
    )
    return "\n".join(lines)


def _clock(seconds: float) -> str:
    minutes = int(seconds // 60)
    return f"{minutes // 60} h {minutes % 60:02d} min"


class _EmptyStepError(Exception):
    """A step with no text and no tool: datapizza would ask again."""


class _StopOnEmptyStep(AgentHooks):
    def after_step(self, context: StepContext, result: StepResult) -> None:
        if not result.text and not result.tools_used:
            raise _EmptyStepError


class _StepLogger(AgentLogger):
    """datapizza's logger prints on the console; this one logs, at debug."""

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        logger.debug("agent_step", agent=self.agent_name, text=str(msg))

    def log_panel(self, *args: Any, **kwargs: Any) -> None:
        logger.debug(
            "agent_step",
            agent=self.agent_name,
            title=kwargs.get("title", ""),
            text=" ".join(str(arg) for arg in args),
        )


class PlantAgent:
    def __init__(
        self,
        reader: PlantReader,
        client: Client,
        generation_args: Mapping[str, Any],
        *,
        max_steps: int = MAX_STEPS,
    ) -> None:
        # Whatever the caller hands in, the agent keeps a reader and no more
        self._reader = ReadOnlyPlant(reader)
        self._client = client
        self._generation_args = dict(generation_args)
        self._max_steps = max_steps

    @property
    def reader(self) -> PlantReader:
        """All the agent can reach of the plant."""
        return self._reader

    async def diagnose(self) -> DiagnosisRun:
        """Diagnose what the plant shows now. A failed API call raises."""
        state = await self._reader.snapshot()
        judged = await watcher.check(self._reader)
        submission = Submission()
        agent = Agent(
            name=NAME,
            client=self._client,
            system_prompt=SYSTEM_PROMPT,
            tools=[*reading_tools(self._reader), submit_tool(submission)],
            max_steps=self._max_steps,
            hooks=_StopOnEmptyStep(),
            logger=_StepLogger(NAME),
        )

        final_text = ""
        # ContextTracing is a singleton whose __new__ has no annotations
        tracing = ContextTracing()  # type: ignore[no-untyped-call]
        with tracing.trace(f"{NAME}.diagnose") as trace:
            try:
                result = await agent.a_run(
                    task(state, judged), tool_choice="auto", **self._generation_args
                )
                final_text = result.text if result else ""
            except _EmptyStepError:
                pass
            # Inside the trace: on its way out, ContextTracing drops the spans
            steps = _steps(trace.get_spans())

        run = _verdict(submission, steps, final_text, self._max_steps)
        logger.info(
            "diagnosis_done",
            outcome=run.outcome,
            steps=len(run.steps),
            input_tokens=run.input_tokens,
            output_tokens=run.output_tokens,
            cached_tokens=run.cached_tokens,
        )
        return run


def _steps(spans: Iterable[Any]) -> tuple[Step, ...]:
    """The steps out of the spans of OpenTelemetry that datapizza records."""
    steps = []
    for span in sorted(spans, key=lambda span: span.start_time or 0):
        attributes = dict(span.attributes or {})
        if attributes.get("type") == "generation":
            stop_reason = str(attributes.get("stop_reason"))
            steps.append(
                Step(
                    kind="model",
                    name=str(attributes.get("model_name", "")),
                    stop_reason=None if stop_reason == "None" else stop_reason,
                    input_tokens=int(attributes.get("prompt_tokens_used", 0)),
                    output_tokens=int(attributes.get("completion_tokens_used", 0)),
                    cached_tokens=int(attributes.get("cached_tokens_used", 0)),
                )
            )
        elif attributes.get("type") == "tool":
            steps.append(
                Step(
                    kind="tool",
                    name=span.name.removeprefix("Tool "),
                    arguments=str(attributes.get("tool_arguments", "")),
                    result=str(attributes.get("tool_result", "")),
                )
            )
    return tuple(steps)


def _verdict(
    submission: Submission, steps: tuple[Step, ...], final_text: str, max_steps: int
) -> DiagnosisRun:
    def run(outcome: Outcome, detail: str) -> DiagnosisRun:
        return DiagnosisRun(
            outcome=outcome,
            diagnosis=submission.diagnosis,
            detail=detail,
            steps=steps,
        )

    calls = [step for step in steps if step.kind == "model"]
    if submission.diagnosis is not None:
        return run(Outcome.DIAGNOSED, "")
    if submission.error:
        return run(Outcome.INVALID_DIAGNOSIS, submission.error)
    if any(step.stop_reason == "refusal" for step in calls):
        return run(Outcome.REFUSED, "Claude ha rifiutato la richiesta.")
    if final_text:
        return run(Outcome.NO_DIAGNOSIS, f"Risposta senza diagnosi: {final_text}")
    return run(
        Outcome.NO_DIAGNOSIS,
        f"Nessuna diagnosi dopo {len(calls)} chiamate su {max_steps} ammesse.",
    )
