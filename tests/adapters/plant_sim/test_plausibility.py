"""Tests for the physics of the simulated plant, and for its time.

Under test: src/neuralbrewery/adapters/plant_sim/ (the whole plant)
Checks 1-5 and 8-10 of docs/impianto.md, "Controlli di plausibilità".

WHY these tests exist: the evals of the agents take the plant as the truth.
A batch that does not add up, or a scenario that changes from one run to
the next, would be read as a mistake of the agent.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.exceptions import ValidationError
from neuralbrewery.core.plant.schemas import Fault, FaultKind, Route, Vessel

DAY = 24 * 3600


class TestHeat:
    async def test_the_hlt_takes_about_45_minutes_to_reach_72_degrees(self, sim, plant):
        """[HP] 35 L from 20 to 72 °C with 3 kW: 42 min with no loss, a few more."""
        hlt = sim.process.vessels[Vessel.HLT]
        assert (await plant.set_temperature(Vessel.HLT, 72)).accepted

        minutes = 0
        while hlt.temp_c < 71.5 and minutes < 90:
            await plant.advance(60)
            minutes += 1

        assert 42 <= minutes <= 48

    async def test_the_mash_in_lands_near_66_degrees(self, sim, plant):
        """[HP] 13.5 L at 72 °C on 4.5 kg of grain at 20 °C give about 66 °C."""
        sim.process.vessels[Vessel.HLT].temp_c = 72.0

        await plant.activate_route(Route.HLT_TO_MASH, 13.5)
        await plant.advance(120)

        tun = sim.process.vessels[Vessel.MASH]
        assert tun.liquid_l == pytest.approx(13.5, abs=0.3)
        assert tun.temp_c == pytest.approx(66, abs=1.5)

    async def test_a_boil_stays_at_100_degrees_and_loses_3_to_4_litres_an_hour(
        self, sim, plant
    ):
        """[HP] At the boil the power left over evaporates water, it heats nothing."""
        kettle = sim.process.vessels[Vessel.BOIL]
        kettle.liquid_l, kettle.temp_c = 26.0, 95.0
        await plant.advance(1)
        assert (await plant.set_temperature(Vessel.BOIL, 100)).accepted
        await plant.advance(600)
        before = kettle.liquid_l

        await plant.advance(3600)

        assert 3.0 <= before - kettle.liquid_l <= 4.0
        assert kettle.temp_c == pytest.approx(100, abs=0.01)
        state = await plant.snapshot()
        assert state.readings["TT3"].value == pytest.approx(100, abs=0.5)


class TestFermentation:
    async def test_five_days_at_19_degrees_along_an_s_curve(self):
        """[HP] From 1.050 to 1.010: slow at the start, half way after 2.5 days."""
        sim = fermentation()
        plant = InProcessPlant(sim)
        wort = sim.process.vessels[Vessel.FERM]
        gravity = {}

        for day in (1.0, 2.5, 5.0):
            await plant.advance(int(day * DAY) - sim.time_s)
            gravity[day] = sim.process.fermentation.gravity
            assert 18.5 < wort.temp_c < 20.0  # regulation holds through the heat

        assert gravity[1.0] > 1.045
        assert gravity[2.5] == pytest.approx(1.030, abs=0.004)
        assert gravity[5.0] == pytest.approx(1.010, abs=0.002)

    async def test_two_healthy_probes_agree_within_their_tolerances(self):
        """[HP] TT5a and TT5b: class A twice over, plus a little noise."""
        plant = InProcessPlant(fermentation())
        apart = []

        for _ in range(60):
            await plant.advance(60)
            readings = (await plant.snapshot()).readings
            apart.append(abs(readings["TT5a"].value - readings["TT5b"].value))

        assert max(apart) < 0.5


class TestVolumes:
    async def test_transfers_lose_nothing(self, sim, plant):
        """[HP] Water in the HLT at the start, the same water spread around after."""
        await plant.activate_route(Route.HLT_TO_MASH, 13.5)
        await plant.advance(120)
        await plant.activate_route(Route.MASH_TO_BOIL, 8)
        await plant.advance(90)

        vessels = sim.process.vessels
        assert sum(vessel.liquid_l for vessel in vessels.values()) == pytest.approx(35)
        assert vessels[Vessel.BOIL].liquid_l == pytest.approx(8, abs=0.3)

    async def test_what_does_not_fit_overflows(self, sim, plant):
        """[EC] A vessel never holds more than its capacity: the rest is lost.

        WHY: a level stuck low hides a full tun from the controller, which
        accepts the transfer. The process must not invent room for it.
        """
        await plant.inject_fault(Fault(kind=FaultKind.LEVEL_STUCK, target="LT2"))
        tun = sim.process.vessels[Vessel.MASH]
        tun.liquid_l = 25.0  # 28 L with the grain, of 30

        assert (await plant.activate_route(Route.HLT_TO_MASH, 10)).accepted
        await plant.advance(120)

        vessels = sim.process.vessels
        assert tun.filled_l == pytest.approx(tun.capacity_l)
        assert sim.process.overflowed_l == pytest.approx(8, abs=0.3)
        assert sum(
            vessel.liquid_l for vessel in vessels.values()
        ) + sim.process.overflowed_l == pytest.approx(35 + 25)


class TestDeterminism:
    @staticmethod
    async def story(seed: int):
        plant = InProcessPlant(brew_day(seed=seed))
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.activate_route(Route.HLT_TO_MASH, 13.5)
        await plant.advance(600)
        return await plant.snapshot(), await plant.events()

    async def test_same_seed_and_same_actions_give_the_same_state(self):
        """[HP] The evals replay a scenario and expect the same plant."""
        assert await self.story(7) == await self.story(7)

    async def test_another_seed_gives_other_noise(self):
        """[EC] The seed is really used: otherwise the test above proves nothing."""
        first, _ = await self.story(7)
        second, _ = await self.story(8)

        assert first.readings != second.readings

    async def test_a_fault_on_one_instrument_leaves_the_noise_of_the_others(self):
        """[EC] Each instrument draws from its own random sequence.

        WHY: with one sequence for all, a fault that draws one number more
        would shift every reading after it, and a scenario with the fault
        could not be compared with the same scenario without.
        """
        healthy = InProcessPlant(brew_day(seed=3))
        faulty = InProcessPlant(brew_day(seed=3))
        await faulty.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT2"))
        await faulty.inject_fault(Fault(kind=FaultKind.LEVEL_FOAM, target="LT1"))

        await healthy.advance(300)
        await faulty.advance(300)

        expected = (await healthy.snapshot()).readings
        found = (await faulty.snapshot()).readings
        for tag in set(expected) - {"TT2", "LT1"}:
            assert found[tag] == expected[tag], tag


class TestTime:
    async def test_time_is_counted_in_whole_steps(self):
        """[HP] Three steps of 10 s are 30 s, with no rounding on the way."""
        plant = InProcessPlant(fermentation(step_s=10))

        await plant.advance(30)

        assert (await plant.snapshot()).sim_time_s == 30

    @pytest.mark.parametrize("seconds", [25, 0.5, -10])
    async def test_a_time_that_is_not_a_number_of_steps_is_an_error(self, seconds):
        """[EC] 25 s with a step of 10 s is refused, not rounded to 20.

        WHY: the prototype rounded, and a scenario "after 25 seconds" ran
        for 20 without a word.
        """
        plant = InProcessPlant(fermentation(step_s=10))

        with pytest.raises(ValidationError):
            await plant.advance(seconds)

        assert (await plant.snapshot()).sim_time_s == 0

    def test_the_step_is_at_least_one_second(self):
        """[EC] A step of zero would stop the time."""
        with pytest.raises(ValueError, match="step"):
            brew_day(step_s=0)
