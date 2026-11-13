"""Tests for the interlocks of the controller.

Under test: src/neuralbrewery/adapters/plant_sim/controller/
The list is in docs/impianto.md, "Interlock"; check 7 asks one test for each.
Interlocks 6, 7 and 9 and the safety contactor K1 need a fault to trip:
their tests are in test_faults.py.

WHY these tests exist: the safety of the plant is here, not in the agent
(AGENTS.md, rule 2). An approved action that the plant should refuse must
be refused whatever the agent, the brewer or the executor believed.
"""

import pytest

from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    CommandCode,
    EventKind,
    Route,
    Vessel,
)
from tests.adapters.plant_sim.conftest import alarms


class TestHeaters:
    async def test_a_setpoint_is_refused_where_the_element_is_not_covered(self, plant):
        """[EC] Interlock 1, at the command: the kettle is empty."""
        result = await plant.set_temperature(Vessel.BOIL, 90)

        assert not result.accepted
        assert result.code is CommandCode.LEVEL_LOW
        assert (await plant.snapshot()).regulation[Vessel.BOIL].setpoint_c is None

    async def test_a_heater_goes_off_when_the_level_falls_below_the_element(
        self, plant
    ):
        """[EC] Interlock 1, while heating: the HLT is emptied to 5 L."""
        assert (await plant.set_temperature(Vessel.HLT, 72)).accepted
        await plant.advance(5)
        assert (await plant.snapshot()).devices.heaters["R1"].commanded_pct == 100

        await plant.activate_route(Route.HLT_TO_BOIL, 30)
        await plant.advance(240)

        state = await plant.snapshot()
        assert state.devices.heaters["R1"].commanded_pct == 0
        assert (AlarmCode.HEATER_BLOCKED, "R1") in alarms(state)
        # Interlock 10: what the controller did on its own is in the events
        raised = [
            event
            for event in await plant.events()
            if event.kind is EventKind.ALARM_RAISED and event.tag == "R1"
        ]
        assert [event.code for event in raised] == [AlarmCode.HEATER_BLOCKED]
        assert 0 < raised[0].sim_time_s < state.sim_time_s

    @pytest.mark.parametrize(
        ("vessel", "celsius"),
        [(Vessel.HLT, 86), (Vessel.HLT, -1), (Vessel.FERM, 31)],
    )
    async def test_a_setpoint_out_of_the_limits_is_refused(
        self, plant, vessel, celsius
    ):
        """[EC] Interlock 8: each vessel has its highest setpoint."""
        result = await plant.set_temperature(vessel, celsius)

        assert not result.accepted
        assert result.code is CommandCode.SETPOINT_OUT_OF_RANGE


class TestMashHeater:
    async def test_the_tun_is_not_heated_while_the_wort_stands_still(self, mashed):
        """[EC] Interlock 2, at the command: no agitator, no recirculation."""
        result = await mashed.set_temperature(Vessel.MASH, 66)

        assert not result.accepted
        assert result.code is CommandCode.WORT_NOT_MOVING

    async def test_recirculation_counts_as_wort_moving(self, mashed):
        """[HP] Interlock 2: the recirculation moves the wort as the agitator does."""
        assert (await mashed.activate_route(Route.MASH_RECIRC)).accepted

        assert (await mashed.set_temperature(Vessel.MASH, 66)).accepted

        await mashed.advance(120)  # it has no quantity: it runs until stopped
        state = await mashed.snapshot()
        assert state.transfer.requested_l is None
        assert state.devices.pumps["P2"].commanded_on
        assert state.devices.heaters["R2"].commanded_pct == 100
        assert state.alarms == ()

    async def test_a_blocked_heater_waits_for_the_brewer(self, mashed):
        """[EC] Interlock 2, while heating; then only reset lets it go on.

        WHY: the controller never restarts by itself. The agitator stops,
        the heater is blocked; the agitator comes back, and the heater
        stays blocked until someone with the authority says so.
        """
        await mashed.set_agitator(True)
        await mashed.advance(1)
        assert (await mashed.set_temperature(Vessel.MASH, 66)).accepted
        await mashed.advance(2)
        assert (await mashed.snapshot()).devices.heaters["R2"].commanded_pct == 100

        await mashed.set_agitator(False)
        await mashed.advance(1)

        state = await mashed.snapshot()
        assert state.devices.heaters["R2"].commanded_pct == 0
        assert (AlarmCode.HEATER_BLOCKED, "R2") in alarms(state)
        assert state.regulation[Vessel.MASH].setpoint_c == 66  # the request stays

        await mashed.set_agitator(True)
        await mashed.advance(5)

        state = await mashed.snapshot()
        assert state.devices.agitator.running
        assert state.devices.heaters["R2"].commanded_pct == 0
        assert (AlarmCode.HEATER_BLOCKED, "R2") in alarms(state)

        assert (await mashed.reset()).accepted
        await mashed.advance(1)

        state = await mashed.snapshot()
        assert state.devices.heaters["R2"].commanded_pct == 100
        assert state.alarms == ()


class TestAgitator:
    async def test_the_agitator_does_not_start_in_an_empty_tun(self, plant):
        """[EC] Interlock 3, at the command: only dry grain in the tun."""
        result = await plant.set_agitator(True)

        assert not result.accepted
        assert result.code is CommandCode.LEVEL_LOW

    async def test_the_agitator_stops_when_the_tun_is_drained(self, mashed):
        """[EC] Interlock 3, while running; a new command re-arms it.

        A command on the same thing is the brewer taking charge, as reset is.
        """
        await mashed.set_agitator(True)
        await mashed.advance(1)
        drive = (await mashed.snapshot()).devices.agitator
        assert (drive.running, drive.frequency_hz) == (True, 50)

        await mashed.activate_route(Route.MASH_TO_BOIL, 8.7)
        await mashed.advance(90)

        state = await mashed.snapshot()
        assert not state.devices.agitator.commanded_run
        assert not state.devices.agitator.running
        assert (AlarmCode.AGITATOR_BLOCKED, "M1") in alarms(state)

        await mashed.activate_route(Route.HLT_TO_MASH, 5)
        await mashed.advance(60)
        assert not (await mashed.snapshot()).devices.agitator.commanded_run

        assert (await mashed.set_agitator(True)).accepted
        await mashed.advance(1)

        state = await mashed.snapshot()
        assert state.devices.agitator.running
        assert state.alarms == ()


class TestTransfers:
    @pytest.mark.parametrize(
        ("route", "liters", "code"),
        [
            (Route.BOIL_TO_FERM, 5, CommandCode.SOURCE_LOW),  # empty kettle
            (Route.HLT_TO_MASH, 28, CommandCode.NO_ROOM),  # 27 L free in the tun
            (Route.HLT_TO_MASH, None, CommandCode.INVALID_QUANTITY),
            (Route.HLT_TO_MASH, 0, CommandCode.INVALID_QUANTITY),
            (Route.MASH_RECIRC, 5, CommandCode.INVALID_QUANTITY),
        ],
    )
    async def test_a_transfer_that_cannot_end_well_is_refused(
        self, plant, route, liters, code
    ):
        """[EC] Interlock 4, at the command; and a transfer needs its quantity."""
        result = await plant.activate_route(route, liters)

        assert not result.accepted
        assert result.code is code
        assert (await plant.snapshot()).transfer is None

    async def test_only_one_route_at_a_time(self, plant):
        """[EC] Interlock 5."""
        assert (await plant.activate_route(Route.HLT_TO_MASH, 5)).accepted

        result = await plant.activate_route(Route.HLT_TO_BOIL, 5)

        assert not result.accepted
        assert result.code is CommandCode.ROUTE_BUSY

    async def test_a_transfer_stops_when_the_source_runs_low(self, sim, plant):
        """[EC] Interlock 4, while pumping: 34 L asked of the 35 in the HLT."""
        assert (await plant.activate_route(Route.HLT_TO_BOIL, 34)).accepted

        await plant.advance(300)

        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert (AlarmCode.TRANSFER_STOPPED, Route.HLT_TO_BOIL) in alarms(state)
        assert 1.3 < sim.process.vessels[Vessel.HLT].liquid_l < 2.7

    async def test_a_transfer_stops_when_the_destination_is_full(self, sim, plant):
        """[EC] Interlock 4, while pumping: someone fills the kettle by hand."""
        assert (await plant.activate_route(Route.HLT_TO_BOIL, 20)).accepted
        await plant.advance(10)

        sim.process.vessels[Vessel.BOIL].liquid_l = 41.0
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert (AlarmCode.TRANSFER_STOPPED, Route.HLT_TO_BOIL) in alarms(state)
