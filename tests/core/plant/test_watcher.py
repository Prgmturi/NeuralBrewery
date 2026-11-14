"""Tests for the watcher: fixed rules that judge the process.

Under test: src/neuralbrewery/core/plant/watcher.py, on the whole simulated
plant, through PlantReader only
Spec: docs/impianto.md, "Allarmi ed eventi" (the judgements on the process)

WHY these tests exist: the controller reports facts, the watcher judges
the process, and its alarm starts a diagnosis. An alarm on a healthy plant
would send the agent after a fault that is not there; one that comes and
goes with the noise would do it twice; and the evals count on the same
alarm from the same seed and the same actions.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    Fault,
    FaultKind,
    ProgramStatus,
    Vessel,
    WatcherAlarm,
    WatcherCode,
)
from tests.adapters.plant_sim.conftest import alarms

MINUTE = 60
HOUR = 3600


async def offset_fermenter(minutes: int, seed: int = 42) -> InProcessPlant:
    """A fermentation where TT5a reads 2 °C more than the truth from the start."""
    plant = InProcessPlant(fermentation(progress=0.3, seed=seed))
    await plant.inject_fault(
        Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
    )
    await plant.advance(minutes * MINUTE)
    return plant


class TestHealthyPlant:
    async def test_a_whole_brew_day_raises_nothing(self):
        """[HP] From cold water to pitched wort, checked every ten minutes."""
        plant = InProcessPlant(brew_day())
        reader: PlantReader = plant
        assert (await plant.start_program()).accepted

        while (state := await plant.snapshot()).program.status is not (
            ProgramStatus.DONE
        ):
            assert state.sim_time_s < 5 * HOUR, state.program
            if state.sim_time_s % (10 * MINUTE) == 0:
                assert await watcher.check(reader) == []
            if state.program.status is ProgramStatus.WAITING:
                assert (await plant.confirm_step()).accepted
            else:
                await plant.advance(5)

        assert await watcher.check(reader) == []

    async def test_twelve_hours_of_fermentation_raise_nothing(self):
        """[HP] Two healthy probes stay within their tolerances: no judgement."""
        plant = InProcessPlant(fermentation(progress=0.3))

        for _ in range(12):
            await plant.advance(HOUR)
            assert await watcher.check(plant) == []


class TestProbesDisagree:
    async def test_an_offset_probe_is_judged_after_ten_minutes(self):
        """[EC] TT5a reads 2 °C high; the controller sees nothing wrong."""
        plant = await offset_fermenter(minutes=12)

        found = await watcher.check(plant)

        assert (await plant.snapshot()).alarms == ()  # no fact for the controller
        assert [(alarm.code, alarm.tag) for alarm in found] == [
            (WatcherCode.PROBES_DISAGREE, Vessel.FERM)
        ]
        # The sample at 0 s was taken before the fault: the next one shows it
        assert found[0].since_s == MINUTE
        assert "TT5a" in found[0].text and "TT5b" in found[0].text

    async def test_not_before_ten_minutes(self):
        """[EC] A disagreement must last: one sample is not a judgement."""
        plant = await offset_fermenter(minutes=9)

        assert await watcher.check(plant) == []

    async def test_the_judgement_counts_from_when_the_probes_parted(self):
        """[EC] Hours of agreement before the fault do not count."""
        plant = InProcessPlant(fermentation(progress=0.3))
        await plant.advance(2 * HOUR)
        await plant.inject_fault(
            Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
        )

        await plant.advance(5 * MINUTE)
        assert await watcher.check(plant) == []

        await plant.advance(6 * MINUTE)
        (found,) = await watcher.check(plant)
        assert found.since_s == 2 * HOUR + MINUTE  # the first sample after the fault

    async def test_a_history_shorter_than_the_fault_counts_from_its_oldest_sample(
        self,
    ):
        """[EC] The history forgets when the probes parted: still a fault."""
        plant = InProcessPlant(fermentation(progress=0.3, history_window_s=15 * MINUTE))
        await plant.inject_fault(
            Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
        )
        await plant.advance(40 * MINUTE)

        (found,) = await watcher.check(plant)

        oldest = (await plant.history("TT5a"))[0]
        assert found.since_s == oldest.sim_time_s > MINUTE

    async def test_a_faulty_probe_is_the_controllers_fact_not_a_judgement(self):
        """[EC] TT5b broken: no value to compare, and the controller says so."""
        plant = InProcessPlant(fermentation(progress=0.3))
        await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT5b"))
        await plant.advance(HOUR)

        assert await watcher.check(plant) == []
        assert (AlarmCode.SIGNAL_FAULT, "TT5b") in alarms(await plant.snapshot())

    async def test_the_judgement_ends_when_the_probe_is_mended(self):
        """[EC] The watcher keeps nothing: it judges what the plant shows now."""
        plant = await offset_fermenter(minutes=15)
        assert await watcher.check(plant) != []

        await plant.clear_faults()
        await plant.advance(MINUTE)

        assert await watcher.check(plant) == []


class TestDeterminism:
    async def test_same_seed_same_actions_same_alarm(self):
        """[HP] The evals start from this alarm: it must not change between runs."""

        async def judged() -> list[WatcherAlarm]:
            return await watcher.check(await offset_fermenter(minutes=20))

        first, second = await judged(), await judged()

        assert first == second
        assert len(first) == 1

    @pytest.mark.parametrize("seed", [1, 7, 42, 1234])
    async def test_every_seed_judges_the_offset(self, seed):
        """[EC] 2 °C is far above two tolerances plus the noise, whatever the seed."""
        plant = await offset_fermenter(minutes=20, seed=seed)

        assert [alarm.code for alarm in await watcher.check(plant)] == [
            WatcherCode.PROBES_DISAGREE
        ]
