"""Tests for what the three ports of the plant promise.

Under test: src/neuralbrewery/adapters/plant_sim/adapter.py
Ports: src/neuralbrewery/core/plant/protocols.py

WHY these tests exist: agents, watcher and executor know the plant only
through these ports. The adapter that calls the plant over REST (milestone
M2) has to pass the same tests as the one that runs it in process.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import fermentation
from neuralbrewery.core.exceptions import NotFoundError
from neuralbrewery.core.plant.protocols import (
    PlantCommander,
    PlantReader,
    SimulationControl,
)
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    EventKind,
    Program,
    ProgramStatus,
    Quality,
    Route,
    Vessel,
)
from tests.adapters.plant_sim.conftest import alarms

SIGNALS_4_20_MA = {"TT1", "TT2", "TT3", "TT5a", "TT5b", "LT1", "LT2", "LT3", "LT4"}
HYDROMETER = {"DT1", "DT1.temperature", "DT1.battery", "DT1.rssi"}


class TestPorts:
    def test_the_in_process_plant_is_all_three_ports(self, plant):
        """[CT] One object, handed to each consumer as the one port it may use."""
        assert isinstance(plant, PlantReader)
        assert isinstance(plant, PlantCommander)
        assert isinstance(plant, SimulationControl)


class TestSnapshot:
    async def test_brew_day_starts_loaded_idle_and_healthy(self, plant):
        """[HP] 35 L in the HLT, dry grain in the tun, everything off."""
        state = await plant.snapshot()

        assert state.sim_time_s == 0
        assert set(state.readings) == SIGNALS_4_20_MA | HYDROMETER
        for tag in SIGNALS_4_20_MA:
            reading = state.readings[tag]
            assert reading.quality is Quality.GOOD, tag
            assert 3.8 <= reading.current_ma <= 20.5, tag
        assert state.readings["LT1"].value == pytest.approx(35, abs=0.7)
        assert state.readings["LT2"].value == pytest.approx(3, abs=0.7)  # the grain
        assert state.readings["LT3"].value == pytest.approx(0, abs=0.7)
        assert state.readings["TT1"].value == pytest.approx(20, abs=0.4)
        assert state.readings["TT1"].unit == "°C"

        devices = state.devices
        assert not any(pump.commanded_on for pump in devices.pumps.values())
        assert not any(valve.commanded_open for valve in devices.valves.values())
        assert all(valve.closed_contact for valve in devices.valves.values())
        assert not any(heater.commanded_pct for heater in devices.heaters.values())
        assert devices.safety_contactor.closed
        assert not devices.agitator.running

        assert {
            vessel: (loop.setpoint_c, loop.probe)
            for vessel, loop in state.regulation.items()
        } == {
            Vessel.HLT: (None, "TT1"),
            Vessel.MASH: (None, "TT2"),
            Vessel.BOIL: (None, "TT3"),
            Vessel.FERM: (None, "TT5a"),
        }
        assert state.transfer is None
        assert state.program == Program(status=ProgramStatus.IDLE)
        assert state.alarms == ()

    async def test_on_brew_day_the_hydrometer_is_not_in_the_fermenter_yet(self, plant):
        """[EC] No message ever: no value, and no alarm for the whole brew."""
        await plant.advance(3600)

        state = await plant.snapshot()
        for tag in HYDROMETER:
            reading = state.readings[tag]
            assert (reading.value, reading.quality) == (None, Quality.STALE), tag
        assert state.alarms == ()

    async def test_fermentation_starts_with_20_litres_held_at_19_degrees(self):
        """[HP] The other named start: hot side empty, the fermenter working."""
        plant = InProcessPlant(fermentation())

        state = await plant.snapshot()

        assert state.readings["LT4"].value == pytest.approx(20, abs=0.7)
        assert state.readings["LT1"].value == pytest.approx(0, abs=0.7)
        assert state.regulation[Vessel.FERM].setpoint_c == 19
        gravity = state.readings["DT1"]
        assert gravity.quality is Quality.GOOD
        assert gravity.value == pytest.approx(1.050, abs=0.003)
        assert state.readings["DT1.battery"].value == pytest.approx(4.1, abs=0.05)
        assert state.readings["DT1.rssi"].unit == "dBm"
        assert state.alarms == ()


class TestCommands:
    async def test_a_transfer_ends_by_itself_at_the_quantity_asked(self, sim, plant):
        """[HP] A command has a certain end: nobody has to say stop."""
        assert (await plant.activate_route(Route.HLT_TO_MASH, 13.5)).accepted
        await plant.advance(30)
        running = (await plant.snapshot()).transfer
        assert (running.route, running.requested_l) == (Route.HLT_TO_MASH, 13.5)
        assert 3 < running.done_l < 6

        await plant.advance(90)

        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert state.devices.valves["EV2a"].closed_contact
        assert sim.process.vessels[Vessel.MASH].liquid_l == pytest.approx(13.5, abs=0.3)
        done = [
            event
            for event in await plant.events()
            if event.kind is EventKind.TRANSFER_DONE
        ]
        assert [event.tag for event in done] == [Route.HLT_TO_MASH]

    async def test_a_transfer_that_ends_a_little_short_is_done(self, sim, mashed):
        """[EC] 0.3 L more than the tun can give are asked: done, with no alarm.

        WHY: litres are counted on a level probe good to half a litre. The
        two drains of the brew ask all the tun can give: without this, in
        2 seeds of 50 the noise of the level made one of them end in alarm.
        """
        gives = sim.process.vessels[Vessel.MASH].drainable_l  # about 9 L
        assert (await mashed.activate_route(Route.MASH_TO_BOIL, gives + 0.3)).accepted

        await mashed.advance(150)

        state = await mashed.snapshot()
        assert state.transfer is None
        assert state.alarms == ()
        assert sim.process.vessels[Vessel.BOIL].liquid_l == pytest.approx(gives)
        done = [
            event
            for event in await mashed.events()
            if event.kind is EventKind.TRANSFER_DONE
        ]
        assert [event.tag for event in done] == [Route.HLT_TO_MASH, Route.MASH_TO_BOIL]

    async def test_a_transfer_that_ends_well_short_is_an_alarm(self, sim, mashed):
        """[EC] Interlock 6 with no fault: 2 L more than the tun can give."""
        gives = sim.process.vessels[Vessel.MASH].drainable_l
        assert (await mashed.activate_route(Route.MASH_TO_BOIL, gives + 2)).accepted

        await mashed.advance(150)

        state = await mashed.snapshot()
        assert state.transfer is None
        assert alarms(state) == {(AlarmCode.TRANSFER_NO_PROGRESS, Route.MASH_TO_BOIL)}
        assert sim.process.vessels[Vessel.BOIL].liquid_l == pytest.approx(gives)

    async def test_stop_route_ends_the_transfer(self, sim, plant):
        """[HP] Stopping is always accepted, with a transfer running or not."""
        await plant.activate_route(Route.HLT_TO_MASH, 13.5)
        await plant.advance(30)

        assert (await plant.stop_route()).accepted
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert state.devices.valves["EV2a"].closed_contact
        assert sim.process.vessels[Vessel.MASH].liquid_l < 6
        assert (await plant.stop_route()).accepted

    async def test_stop_all_stops_the_hot_side_and_leaves_the_fermenter(
        self, sim, mashed
    ):
        """[EC] A stop on brew day must not switch off a fermentation.

        WHY: in the prototype stop_all cleared the setpoint of the fermenter
        too, and a day later the beer was at 21 °C.
        """
        sim.process.vessels[Vessel.FERM].liquid_l = 20.0
        await mashed.set_agitator(True)
        await mashed.advance(1)
        assert (await mashed.set_temperature(Vessel.HLT, 72)).accepted
        assert (await mashed.set_temperature(Vessel.MASH, 66)).accepted
        assert (await mashed.set_temperature(Vessel.FERM, 19)).accepted
        assert (await mashed.activate_route(Route.HLT_TO_BOIL, 5)).accepted
        await mashed.advance(5)

        assert (await mashed.stop_all()).accepted
        await mashed.advance(1)

        state = await mashed.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert not state.devices.agitator.commanded_run
        assert state.devices.heaters["R1"].commanded_pct == 0
        assert state.regulation[Vessel.HLT].setpoint_c is None
        assert state.regulation[Vessel.MASH].setpoint_c is None
        assert state.regulation[Vessel.FERM].setpoint_c == 19
        assert state.alarms == ()

    async def test_a_setpoint_can_be_taken_away(self, plant):
        """[HP] None is "off": always accepted."""
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.advance(5)

        assert (await plant.set_temperature(Vessel.HLT, None)).accepted
        await plant.advance(1)

        state = await plant.snapshot()
        assert state.regulation[Vessel.HLT].setpoint_c is None
        assert state.devices.heaters["R1"].commanded_pct == 0


class TestEventsAndHistory:
    async def test_every_accepted_command_is_an_event(self, plant):
        """[HP] In order, numbered, with the simulated time."""
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.set_temperature(Vessel.BOIL, 90)  # refused: not an event
        await plant.advance(10)
        await plant.stop_all()

        events = await plant.events()

        assert [(event.kind, event.code, event.sim_time_s) for event in events] == [
            (EventKind.COMMAND, "set_temperature", 0),
            (EventKind.COMMAND, "stop_all", 10),
        ]
        assert events[0].tag == Vessel.HLT
        assert events[0].seq < events[1].seq
        assert await plant.events(since_s=5) == events[1:]

    async def test_the_history_keeps_one_sample_a_minute(self, plant):
        """[HP] Readings as they were, commands as their mean over the minute."""
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.advance(600)

        temperature = await plant.history("TT1")
        heater = await plant.history("R1")

        assert [sample.sim_time_s for sample in temperature] == list(range(0, 601, 60))
        values = [sample.value for sample in temperature]
        assert values == sorted(values)
        assert values[-1] - values[0] == pytest.approx(12, abs=1)  # 3 kW on 35 L
        assert [sample.value for sample in heater[1:]] == [100] * 10
        assert await plant.history("TT1", since_s=540) == temperature[-2:]

    async def test_the_history_shows_how_long_a_heater_was_on(self, sim, plant):
        """[EC] Holding 72 °C the heater is on a part of each minute."""
        sim.process.vessels[Vessel.HLT].temp_c = 71.9
        await plant.advance(1)
        await plant.set_temperature(Vessel.HLT, 72)

        await plant.advance(1800)

        shares = [sample.value for sample in await plant.history("R1")]
        assert any(0 < share < 100 for share in shares)

    async def test_a_tag_with_no_history_is_not_found(self, plant):
        """[EC] The valves of the routes are not recorded: only EV9 is."""
        with pytest.raises(NotFoundError):
            await plant.history("EV3")
