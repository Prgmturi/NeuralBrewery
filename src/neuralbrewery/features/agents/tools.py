"""The tools of the plant agent: four that read, one that hands in.

The reading tools close over a PlantReader and nothing else. Each answers
in JSON, in simulated time, and turns an error into an answer for the
model: datapizza would let an exception end the whole diagnosis. The MCP
server serves the same functions (mcp_server.py), so both read alike.

submit_diagnosis ends the loop. Its arguments are flat, so the model sees
one simple schema; they are checked here, with pydantic, because datapizza
does not ask the API to enforce the schema of a tool. Its schema is written
from SubmitArguments, not read from a signature: for an optional enum
datapizza leaves references that the JSON encoder cannot write.
"""

import json
from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from datapizza.tools import Tool
from pydantic import BaseModel, Field, ValidationError

from neuralbrewery.core.exceptions import NotFoundError
from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.schemas import Command, Proposal, Route, Vessel
from neuralbrewery.features.agents.diagnosis import Diagnosis, FaultType

MINUTE = 60.0

# What the model reads of each argument, twice: datapizza takes the first
# item of Annotated, the MCP server (pydantic) the Field
SINCE = "Da quanti minuti fa, contando dal tempo simulato di adesso"
TAG = "La sigla: una lettura (TT5a, LT1, DT1...) o un comando (R2, P1, EV9)"
SinceMinutes = Annotated[float, SINCE, Field(description=SINCE)]
Tag = Annotated[str, TAG, Field(description=TAG)]

ReadingFunction = Callable[..., Awaitable[str]]


def reading_tools(reader: PlantReader) -> list[Tool]:
    """The reading functions as tools of datapizza."""
    return [Tool(function) for function in reading_functions(reader)]


def reading_functions(reader: PlantReader) -> list[ReadingFunction]:
    """Four functions that read the plant, with the docstrings the model reads."""

    async def since_s(minutes: float) -> float:
        now = (await reader.snapshot()).sim_time_s
        return max(0.0, now - minutes * MINUTE)

    async def read_plant() -> str:
        """La fotografia del controllore adesso: tempo simulato (sim_time_s, in
        secondi), letture con qualità e corrente, dispositivi (comando e, dove
        c'è, ritorno), regolazione (setpoint e sonda in uso), travaso, programma
        della cotta, allarmi attivi."""
        return (await reader.snapshot()).model_dump_json()

    async def read_events(since_minutes: SinceMinutes = 60.0) -> str:
        """Gli eventi del controllore, dal più vecchio: allarmi che nascono e
        finiscono, comandi accettati (anche del programma), travasi completati,
        passi del programma."""
        events = await reader.events(await since_s(since_minutes))
        return json.dumps(
            [event.model_dump(mode="json") for event in events], ensure_ascii=False
        )

    async def read_history(tag: Tag, since_minutes: SinceMinutes = 60.0) -> str:
        """Lo storico breve di una sigla, un campione al minuto, come coppie
        [sim_time_s, valore]. Una lettura è com'era; un comando di resistenza,
        pompa o EV9 è la media in percento dal campione prima. null: lettura
        senza valore."""
        try:
            samples = await reader.history(tag, await since_s(since_minutes))
        except NotFoundError:
            return (
                f"Nessuno storico per {tag}. Si registrano le letture e i comandi "
                "di resistenze, pompe ed EV9."
            )
        pairs = [[sample.sim_time_s, sample.value] for sample in samples]
        return json.dumps({"tag": tag, "samples": pairs})

    async def run_watcher() -> str:
        """I giudizi del sorvegliante sul processo adesso: regole fisse, per
        esempio due sonde dello stesso recipiente che non concordano."""
        judged = await watcher.check(reader)
        return json.dumps(
            [alarm.model_dump(mode="json") for alarm in judged], ensure_ascii=False
        )

    return [read_plant, read_events, read_history, run_watcher]


class SubmitArguments(BaseModel):
    """What the model fills in to hand in a diagnosis, and what it reads of each."""

    component: str = Field(
        description="La sigla del componente guasto (per esempio TT5a, P1, M1), "
        "o il percorso"
    )
    fault_type: FaultType = Field(
        description="measurement: lo strumento mente e l'impianto è sano. "
        "process: l'impianto è guasto e le misure sono giuste"
    )
    confirmed: bool = Field(
        description="true solo se i dati bastano a dire la causa con certezza"
    )
    explanation: str = Field(
        description="La spiegazione per il birraio, in italiano, breve"
    )
    checks: list[str] = Field(
        description="Le verifiche a mano per il birraio, in italiano; "
        "vuota se non ne servono"
    )
    command: Command | None = Field(
        default=None,
        description="Il pulsante del pannello da proporre; "
        "null se prima servono verifiche",
    )
    route: Route | None = Field(
        default=None, description="Per activate_route: il percorso"
    )
    liters: float | None = Field(
        default=None, description="Per activate_route: i litri; null per il ricircolo"
    )
    vessel: Vessel | None = Field(
        default=None, description="Per set_temperature: il recipiente"
    )
    celsius: float | None = Field(
        default=None, description="Per set_temperature: i gradi; null spegne"
    )
    on: bool | None = Field(
        default=None, description="Per set_agitator: acceso o spento"
    )

    def diagnosis(self) -> Diagnosis:
        """Raises ValidationError when the plant could not take it."""
        proposal = (
            None
            if self.command is None
            else Proposal(
                command=self.command,
                route=self.route,
                liters=self.liters,
                vessel=self.vessel,
                celsius=self.celsius,
                on=self.on,
            )
        )
        return Diagnosis(
            component=self.component,
            fault_type=self.fault_type,
            confirmed=self.confirmed,
            explanation=self.explanation,
            checks=tuple(self.checks),
            proposal=proposal,
        )


def flat_schema(model: type[BaseModel]) -> dict[str, Any]:
    """The JSON schema of the model, with each $ref replaced by what it names."""
    schema = model.model_json_schema()
    definitions = schema.pop("$defs", {})

    def inline(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                return inline(definitions[node["$ref"].rsplit("/", 1)[-1]])
            return {key: inline(value) for key, value in node.items()}
        if isinstance(node, list):
            return [inline(item) for item in node]
        return node

    flat: dict[str, Any] = inline(schema)
    return flat


class Submission:
    """What the agent handed in: a diagnosis, or why it was not one."""

    def __init__(self) -> None:
        self.diagnosis: Diagnosis | None = None
        self.error = ""


def submit_tool(submission: Submission) -> Tool:
    def submit_diagnosis(**arguments: Any) -> str:
        if submission.diagnosis is not None or submission.error:
            return "Diagnosi già consegnata."
        try:
            submission.diagnosis = SubmitArguments.model_validate(arguments).diagnosis()
        except ValidationError as error:
            submission.error = str(error)
            return f"Diagnosi non valida: {error}"
        return "Diagnosi consegnata."

    schema = flat_schema(SubmitArguments)
    return Tool(
        submit_diagnosis,
        name="submit_diagnosis",
        description="Consegna la diagnosi e la chiude: chiamalo una volta sola, "
        "alla fine.",
        properties=schema["properties"],
        required=schema["required"],
        end=True,
    )
