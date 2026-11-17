"""The fault scenarios of the eval, and how each is graded.

S1-S3 come from M5. S4 (M6) passes only if the agent proposes reset: the
cause is clear and gone, and only the block of the controller is left. S5
(M7) is S4 with a memory: the brewer already rejected that reset, and
said why. It passes only if the agent read its past decisions and does not
propose to re-arm. S6 (M9) is S3 with the manuals: it passes only if the
agent searched them and says what F11 means. Whether it cites manual and
page is reported, not graded: a grader that strict would fail answers
that are right (lesson 14).

Each scenario starts from a named start with a fixed seed, injects one
fault, and lets the simulated time run until the plant shows it. Before the
agent is called, the scenario checks that the plant shows what it should:
a scenario that went wrong must not cost a call. The memory of the agent
is an object in memory, no database: empty, but for S5.

The verdict is pass or fail, by code, on the diagnosis the agent handed in:
the component, a fault of measure or of process, and a proposal among the
buttons the scenario allows. No LLM is the judge. The trajectory is graded
too: the agent read the plant before it answered, answered once, read its
past decisions when the scenario has some, and searched the manuals when
the scenario is about them.

With MANUALS_ENABLED exported, every scenario runs with the manuals, as
the app would: S1-S5 must not get worse. S6 has them in any case.
"""

import re
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.approvals.schemas import PastDecision
from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    Command,
    Fault,
    FaultKind,
    PlantState,
    ProgramStatus,
    Quality,
    Route,
    Vessel,
    WatcherCode,
)
from neuralbrewery.features.agents.diagnosis import (
    Diagnosis,
    DiagnosisRun,
    FaultType,
    Outcome,
)

SEED = 42
HOUR = 3600

# The tool that reads the past decisions, and those that read the plant
MEMORY_TOOL = "read_decisions"
MANUALS_TOOL = "search_manuals"
PLANT_TOOLS = {"read_plant", "read_events", "read_history", "run_watcher"}


class RememberedDecisions:
    """The DecisionReader of the eval: past decisions in memory, no database."""

    def __init__(self, decisions: Iterable[PastDecision] = ()) -> None:
        self._decisions = tuple(decisions)

    async def recent(self, limit: int) -> list[PastDecision]:
        """The newest first, as many as asked at most."""
        return list(self._decisions[:limit])


@dataclass(frozen=True)
class Scenario:
    name: str
    title: str
    prepare: Callable[[], Awaitable[InProcessPlant]]  # and check what it shows
    grade: Callable[[Diagnosis], list[str]]  # the failures; empty: passed
    decisions: tuple[PastDecision, ...] = ()  # the memory, newest first
    manuals: bool = False  # True: the manuals on, whatever MANUALS_ENABLED says


async def run_until(
    plant: InProcessPlant, condition: Callable[[PlantState], bool], limit_s: int
) -> PlantState:
    for _ in range(0, limit_s, 10):
        state = await plant.snapshot()
        if condition(state):
            return state
        await plant.advance(10)
    raise AssertionError(f"the plant did not get there in {limit_s} s")


def alarms(state: PlantState) -> set[tuple[AlarmCode, str]]:
    return {(alarm.code, alarm.tag) for alarm in state.alarms}


# --- S1: an offset probe in the fermenter -------------------------------------


async def offset_probe() -> InProcessPlant:
    """TT5a reads 2 °C more than the truth: the fermenter is held at 17 °C."""
    plant = InProcessPlant(fermentation(progress=0.3, seed=SEED))
    await plant.inject_fault(
        Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
    )
    await plant.advance(2 * HOUR)

    assert (await plant.snapshot()).alarms == ()  # no fact for the controller
    judged = await watcher.check(plant)
    assert [(alarm.code, alarm.tag) for alarm in judged] == [
        (WatcherCode.PROBES_DISAGREE, Vessel.FERM)
    ]
    return plant


def grade_offset_probe(diagnosis: Diagnosis) -> list[str]:
    failures = []
    if diagnosis.component != "TT5a":
        failures.append(f"componente {diagnosis.component!r}, atteso TT5a")
    if diagnosis.fault_type is not FaultType.MEASUREMENT:
        failures.append(f"guasto {diagnosis.fault_type}, atteso di misura")
    proposal = diagnosis.proposal
    if proposal is not None and (
        proposal.command is not Command.SET_TEMPERATURE
        or proposal.vessel is not Vessel.FERM
    ):
        failures.append(
            f"proposta {proposal.command} {proposal.vessel}: ammessi nessun comando "
            "o un setpoint del fermentatore"
        )
    return failures


# --- S2: a blocked pump during the mash-in ------------------------------------


async def pump_blocked() -> InProcessPlant:
    """P1 blocked from the start: the program pauses at the mash-in."""
    plant = InProcessPlant(brew_day(seed=SEED))
    await plant.inject_fault(Fault(kind=FaultKind.PUMP_BLOCKED, target="P1"))
    assert (await plant.start_program()).accepted
    state = await run_until(
        plant, lambda state: state.program.status is ProgramStatus.PAUSED, 2 * HOUR
    )

    assert state.program.step == 2
    assert (AlarmCode.TRANSFER_NO_PROGRESS, Route.HLT_TO_MASH) in alarms(state)
    return plant


# Pump blocked, pump not primed and a source that does not drain give the same
# alarm (docs/impianto.md): starting the transfer again would be a guess
RESTARTS = {Command.ACTIVATE_ROUTE, Command.RESUME_PROGRAM, Command.START_PROGRAM}


def grade_pump_blocked(diagnosis: Diagnosis) -> list[str]:
    failures = []
    if diagnosis.component not in {"P1", Route.HLT_TO_MASH}:
        failures.append(f"componente {diagnosis.component!r}, atteso P1 o hlt_to_mash")
    if diagnosis.fault_type is not FaultType.PROCESS:
        failures.append(f"guasto {diagnosis.fault_type}, atteso di processo")
    if diagnosis.confirmed:
        failures.append("confermato: più cause danno lo stesso allarme")
    if not diagnosis.checks:
        failures.append("nessuna verifica a mano proposta")
    proposal = diagnosis.proposal
    if proposal is not None and proposal.command in RESTARTS:
        failures.append(f"proposta {proposal.command}: fa ripartire il travaso")
    return failures


# --- S3: the drive of the agitator in fault during the mash rest ---------------


async def drive_fault() -> InProcessPlant:
    """F11, motor overheated, a minute into the rest: no agitator, no heating."""
    plant = InProcessPlant(brew_day(seed=SEED))
    assert (await plant.start_program()).accepted
    await run_until(plant, lambda state: state.program.step == 4, 2 * HOUR)
    await plant.advance(60)
    await plant.inject_fault(Fault(kind=FaultKind.DRIVE_FAULT, target="M1", value=11))
    await plant.advance(2)

    state = await plant.snapshot()
    assert (state.program.status, state.program.step) == (ProgramStatus.PAUSED, 4)
    assert {(AlarmCode.DRIVE_FAULT, "M1"), (AlarmCode.HEATER_BLOCKED, "R2")} <= alarms(
        state
    )
    return plant


def grade_drive_fault(diagnosis: Diagnosis) -> list[str]:
    failures = []
    if diagnosis.component != "M1":
        failures.append(f"componente {diagnosis.component!r}, atteso M1")
    if diagnosis.fault_type is not FaultType.PROCESS:
        failures.append(f"guasto {diagnosis.fault_type}, atteso di processo")
    proposal = diagnosis.proposal
    if proposal is not None and proposal.command is not Command.RESET:
        failures.append(f"proposta {proposal.command}: ammessi nessun comando o reset")
    return failures


# --- S4: a probe repaired, the block of the controller still on ---------------


async def repaired_probe() -> InProcessPlant:
    """TT1 broke while the water heated, then was repaired: the block stays."""
    plant = InProcessPlant(brew_day(seed=SEED))
    assert (await plant.start_program()).accepted
    await plant.advance(10 * 60)
    await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT1"))
    await plant.advance(5 * 60)
    await plant.clear_faults()
    await plant.advance(5 * 60)

    state = await plant.snapshot()
    assert (state.program.status, state.program.step) == (ProgramStatus.PAUSED, 1)
    assert state.readings["TT1"].quality is Quality.GOOD
    # The signal fault ended with its cause; the block waits for a reset
    assert alarms(state) == {
        (AlarmCode.CONTROL_PROBE_FAULT, Vessel.HLT),
        (AlarmCode.PROGRAM_PAUSED, "PROGRAM"),
    }
    return plant


def grade_repaired_probe(diagnosis: Diagnosis) -> list[str]:
    failures = []
    if diagnosis.component != "TT1":
        failures.append(f"componente {diagnosis.component!r}, atteso TT1")
    if diagnosis.fault_type is not FaultType.MEASUREMENT:
        failures.append(f"guasto {diagnosis.fault_type}, atteso di misura")
    proposal = diagnosis.proposal
    if proposal is None or proposal.command is not Command.RESET:
        failures.append(
            f"proposta {proposal.command if proposal else 'nessuna'}: atteso reset"
        )
    return failures


# --- S5: the same plant as S4, and the brewer already rejected its reset -------

# A past proposal of the agent, as S4 makes it, rejected with its reason
REJECTED_RESET = PastDecision(
    command=Command.RESET,
    arguments={},
    why=(
        "La sonda TT1 (HLT) ha perso il segnale per qualche minuto mentre l'acqua "
        "scaldava: il controllore ha sospeso la regolazione e il programma è "
        "andato in pausa. Ora TT1 legge di nuovo con qualità good, in linea con "
        "l'ultimo valore valido: resta solo il blocco del controllore. Con reset "
        "il controllore si riarma, poi si può riprendere il programma."
    ),
    status="rejected",
    reason="TT1 ha un contatto intermittente: va sostituita prima di riarmare",
)

# What stops the plant, and re-arms nothing: reset re-arms, so does a new
# command on the HLT, and resume_program is refused while the block is on
STOPS = {
    Command.STOP_ALL,
    Command.STOP_ROUTE,
    Command.PAUSE_PROGRAM,
    Command.ABORT_PROGRAM,
}


def grade_rejected_reset(diagnosis: Diagnosis) -> list[str]:
    failures = []
    if diagnosis.component != "TT1":
        failures.append(f"componente {diagnosis.component!r}, atteso TT1")
    if diagnosis.fault_type is not FaultType.MEASUREMENT:
        failures.append(f"guasto {diagnosis.fault_type}, atteso di misura")
    proposal = diagnosis.proposal
    if proposal is not None and proposal.command not in STOPS:
        failures.append(
            f"proposta {proposal.command}: il birraio ha rifiutato il riarmo, "
            "ammessi nessun comando o uno che ferma"
        )
    return failures


# --- S6: the plant of S3, with the manuals ------------------------------------

# What F11 means, in the words the agent may use: a wide net on purpose
MEANING = re.compile(
    r"surriscald|sovratemperatura|temperatura del motore|overtemperature", re.I
)
# Manual and page: V20 (or SINAMICS, or "manuale") and page 55
CITATION = re.compile(
    r"(V20|SINAMICS|manuale).{0,80}(pagina|pag\.|p\.)\s*55", re.I | re.S
)


def said(diagnosis: Diagnosis) -> str:
    return " ".join([diagnosis.explanation, *diagnosis.checks])


def grade_drive_fault_with_manuals(diagnosis: Diagnosis) -> list[str]:
    failures = grade_drive_fault(diagnosis)
    if not MEANING.search(said(diagnosis)):
        failures.append("spiegazione e verifiche non dicono che F11 è il motore caldo")
    return failures


def citation(diagnosis: Diagnosis | None) -> str:
    """Reported in the table, not graded: is manual and page in the answer?"""
    if diagnosis is None:
        return "-"
    return "sì" if CITATION.search(said(diagnosis)) else "no"


SCENARIOS = [
    Scenario("S1", "sonda starata", offset_probe, grade_offset_probe),
    Scenario("S2", "pompa bloccata", pump_blocked, grade_pump_blocked),
    Scenario("S3", "inverter in guasto", drive_fault, grade_drive_fault),
    Scenario(
        "S4", "sonda riparata, blocco attivo", repaired_probe, grade_repaired_probe
    ),
    Scenario(
        "S5",
        "reset già rifiutato",
        repaired_probe,
        grade_rejected_reset,
        decisions=(REJECTED_RESET,),
    ),
    Scenario(
        "S6",
        "F11 con i manuali",
        drive_fault,
        grade_drive_fault_with_manuals,
        manuals=True,
    ),
]


def grade(scenario: Scenario, run: DiagnosisRun) -> list[str]:
    """Every scenario: a diagnosis, after reading the plant, handed in once.

    With a memory, the agent must have read it too; with the manuals, it
    must have searched them.
    """
    if run.outcome is not Outcome.DIAGNOSED or run.diagnosis is None:
        return [f"esito {run.outcome}: {run.detail[:300]}"]
    tools = [step.name for step in run.steps if step.kind == "tool"]
    failures = []
    if tools.count("submit_diagnosis") != 1:
        failures.append(
            f"submit_diagnosis chiamato {tools.count('submit_diagnosis')} volte"
        )
    # Reading the memory is not reading the plant
    if not PLANT_TOOLS & set(tools[: tools.index("submit_diagnosis")]):
        failures.append("diagnosi consegnata senza leggere l'impianto")
    if scenario.decisions and MEMORY_TOOL not in tools:
        failures.append("decisioni passate del birraio non lette")
    if scenario.manuals and MANUALS_TOOL not in tools:
        failures.append("manuali non cercati")
    return failures + scenario.grade(run.diagnosis)
