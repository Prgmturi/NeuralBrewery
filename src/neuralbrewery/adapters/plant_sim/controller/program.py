"""The brew program: its recipe, and where the controller is in it.

One recipe, the reference batch of docs/impianto.md. A step states the
whole hot side (setpoints, agitator, route), not what changes from the step
before: so the controller can put the plant back as the step wants it
after any pause, whatever was switched off in the meantime.

Here are the data and the count. The controller gives the commands
(controller.py, "The brew program").
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

from neuralbrewery.adapters.plant_sim.controller.journal import AlarmKey
from neuralbrewery.adapters.plant_sim.layout import PROGRAM
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    Program,
    ProgramStatus,
    Route,
    Vessel,
)

MINUTE = 60


@dataclass(frozen=True)
class Step:
    name: str
    # What the step wants. A vessel of the hot side that is not here is off.
    setpoints: Mapping[Vessel, float] = field(default_factory=dict)
    agitator: bool = False
    route: Route | None = None
    liters: float | None = None  # with a route and no litres: a recirculation
    # How it ends. With litres: when they have been moved. Otherwise at most
    # one of these two, and with neither the step waits for the brewer.
    reach: tuple[Vessel, float] | None = None  # the vessel gets to that temperature
    lasts_s: int | None = None
    max_s: int | None = None  # past this the step is late

    @property
    def waits_for_brewer(self) -> bool:
        return self.liters is None and self.reach is None and self.lasts_s is None


HLT, MASH, BOIL, FERM = Vessel.HLT, Vessel.MASH, Vessel.BOIL, Vessel.FERM

RECIPE: tuple[Step, ...] = (
    Step("Scalda l'acqua", {HLT: 72}, reach=(HLT, 72), max_s=60 * MINUTE),
    Step(
        "Impasto",
        {HLT: 72},
        route=Route.HLT_TO_MASH,
        liters=13.5,
        max_s=5 * MINUTE,
    ),
    # The agitator starts here: during the mash-in the level is below its blades
    Step(
        "Porta il tino a 66 °C",
        {HLT: 78, MASH: 66},
        agitator=True,
        reach=(MASH, 66),
        max_s=15 * MINUTE,
    ),
    Step("Sosta", {HLT: 78, MASH: 66}, agitator=True, lasts_s=60 * MINUTE),
    Step(
        "Fine sosta",
        {HLT: 78, MASH: 76},
        agitator=True,
        reach=(MASH, 76),
        max_s=15 * MINUTE,
    ),
    Step(
        "Ricircolo",
        {HLT: 78, MASH: 76},
        route=Route.MASH_RECIRC,
        lasts_s=10 * MINUTE,
    ),
    Step(
        "Primo mosto",
        {HLT: 78},
        route=Route.MASH_TO_BOIL,
        liters=9,
        max_s=5 * MINUTE,
    ),
    Step("Lavaggio", route=Route.HLT_TO_MASH, liters=18, max_s=5 * MINUTE),
    Step("Ricircolo", route=Route.MASH_RECIRC, lasts_s=10 * MINUTE),
    Step("Secondo mosto", route=Route.MASH_TO_BOIL, liters=18, max_s=5 * MINUTE),
    Step("Porta a bollore", {BOIL: 100}, reach=(BOIL, 99.5), max_s=30 * MINUTE),
    Step("Bollitura", {BOIL: 100}, lasts_s=60 * MINUTE),
    Step("Pronto al travaso"),
    Step("Al fermentatore", route=Route.BOIL_TO_FERM, liters=20, max_s=5 * MINUTE),
    # The fermenter is held at 19 °C while it waits for the yeast: the
    # brewer's confirm is the pitch, and it ends the program
    Step("Lievito", {FERM: 19}),
)


@dataclass
class Progress:
    """Where the program is. It keeps the count: the controller moves it on."""

    status: ProgramStatus = ProgramStatus.IDLE
    index: int = 0
    given: bool = False  # the commands of the step have been given
    elapsed_s: float = 0.0  # in the step, pauses left out
    moved_l: float = 0.0  # litres of the step moved before a pause
    reason: str = ""  # why it is paused
    by_alarm: bool = False  # paused by the controller, not by the brewer

    @property
    def step(self) -> Step:
        return RECIPE[self.index]

    @property
    def running(self) -> bool:
        return self.status is ProgramStatus.RUNNING

    @property
    def open(self) -> bool:
        """Started and not yet closed: running, or paused."""
        return self.status in (ProgramStatus.RUNNING, ProgramStatus.PAUSED)

    @property
    def waiting(self) -> bool:
        """At a step that only the brewer's confirm ends."""
        return self.running and self.given and self.step.waits_for_brewer

    @property
    def label(self) -> str:
        return f"passo {self.index + 1} ({self.step.name})"

    def start(self) -> None:
        self.status = ProgramStatus.RUNNING
        self._begin(0)

    def advance(self) -> None:
        """To the next step; after the last one the program is done."""
        if self.index + 1 < len(RECIPE):
            self._begin(self.index + 1)
        else:
            self.status = ProgramStatus.DONE

    def _begin(self, index: int) -> None:
        self.index, self.given, self.elapsed_s, self.moved_l = index, False, 0.0, 0.0

    def pause(self, reason: str, *, by_alarm: bool) -> None:
        """The commands of the step are to give again when it resumes."""
        self.status, self.given = ProgramStatus.PAUSED, False
        self.reason, self.by_alarm = reason, by_alarm

    def resume(self) -> None:
        self.status, self.reason, self.by_alarm = ProgramStatus.RUNNING, "", False

    def abort(self) -> None:
        """Close a program that is open. One that is not stays as it is."""
        if self.open:
            self.status, self.reason, self.by_alarm = ProgramStatus.ABORTED, "", False

    def alarms(self) -> dict[AlarmKey, str]:
        """A step past its longest time, and a pause the brewer did not ask for."""
        alarms: dict[AlarmKey, str] = {}
        max_s = self.step.max_s
        if self.open and max_s is not None and self.elapsed_s > max_s:
            alarms[(AlarmCode.STEP_LATE, PROGRAM)] = (
                f"{self.label} oltre il tempo massimo di {max_s // MINUTE} min"
            )
        if self.status is ProgramStatus.PAUSED and self.by_alarm:
            alarms[(AlarmCode.PROGRAM_PAUSED, PROGRAM)] = (
                f"programma in pausa al {self.label}: {self.reason}"
            )
        return alarms

    def view(self) -> Program:
        if self.status is ProgramStatus.IDLE:
            return Program(status=ProgramStatus.IDLE)
        return Program(
            status=ProgramStatus.WAITING if self.waiting else self.status,
            step=self.index + 1,
            step_name=self.step.name,
            elapsed_s=self.elapsed_s,
            max_s=self.step.max_s,
            reason=self.reason,
        )
