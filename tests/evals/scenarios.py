"""The three fault scenarios of the M5 eval, and how each is graded.

Each scenario starts from a named start with a fixed seed, injects one
fault, and lets the simulated time run until the plant shows it. Before the
agent is called, the scenario checks that the plant shows what it should:
a scenario that went wrong must not cost a call.

The verdict is pass or fail, by code, on the diagnosis the agent handed in:
the component, a fault of measure or of process, and a proposal among the
buttons the scenario allows. No LLM is the judge. The trajectory is graded
too: the agent read the plant before it answered, and answered once.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    Command,
    Fault,
    FaultKind,
    PlantState,
    ProgramStatus,
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


@dataclass(frozen=True)
class Scenario:
    name: str
    title: str
    prepare: Callable[[], Awaitable[InProcessPlant]]  # and check what it shows
    grade: Callable[[Diagnosis], list[str]]  # the failures; empty: passed


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


SCENARIOS = [
    Scenario("S1", "sonda starata", offset_probe, grade_offset_probe),
    Scenario("S2", "pompa bloccata", pump_blocked, grade_pump_blocked),
    Scenario("S3", "inverter in guasto", drive_fault, grade_drive_fault),
]


def grade(scenario: Scenario, run: DiagnosisRun) -> list[str]:
    """Every scenario: a diagnosis, after reading the plant, handed in once."""
    if run.outcome is not Outcome.DIAGNOSED or run.diagnosis is None:
        return [f"esito {run.outcome}: {run.detail[:300]}"]
    tools = [step.name for step in run.steps if step.kind == "tool"]
    failures = []
    if tools.count("submit_diagnosis") != 1:
        failures.append(
            f"submit_diagnosis chiamato {tools.count('submit_diagnosis')} volte"
        )
    if tools.index("submit_diagnosis") == 0:
        failures.append("diagnosi consegnata senza leggere l'impianto")
    return failures + scenario.grade(run.diagnosis)
