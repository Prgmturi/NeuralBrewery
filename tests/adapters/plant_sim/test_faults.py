"""Tests for the faults a test or an eval can inject.

Under test: src/neuralbrewery/adapters/plant_sim/ (the whole plant)
One test for each row of the two tables of docs/impianto.md, "Guasti
iniettabili" (check 11): the controller must show what the row says, and
nothing more. Interlocks 6, 7 and 9 and the safety contactor K1 trip here.

WHY these tests exist: these are the scenarios of the evals. An agent is
judged on the cause it finds from what the controller shows: if a fault
showed something else, the right diagnosis would be marked wrong.
"""

from statistics import mean, median

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import fermentation
from neuralbrewery.core.exceptions import ValidationError
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    CommandCode,
    Fault,
    FaultKind,
    Quality,
    Route,
    Vessel,
)
from tests.adapters.plant_sim.conftest import alarms

HOUR = 3600


class TestMeasurementFaults:
    async def test_pt100_broken_wire(self, plant):
        """[EC] At least 21.5 mA: the transmitter says "I am faulty", not why."""
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.advance(5)

        await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT1"))
        await plant.advance(1)

        state = await plant.snapshot()
        reading = state.readings["TT1"]
        assert (reading.quality, reading.value) == (Quality.BAD, None)
        assert reading.reason == "strumento guasto"
        assert reading.current_ma >= 21.5
        assert {
            (AlarmCode.SIGNAL_FAULT, "TT1"),
            (AlarmCode.CONTROL_PROBE_FAULT, Vessel.HLT),
        } <= alarms(state)
        assert state.devices.heaters["R1"].commanded_pct == 0
        refused = await plant.set_temperature(Vessel.HLT, 70)
        assert refused.code is CommandCode.PROBE_FAULT

    async def test_pt100_broken_wire_in_the_fermenter_moves_to_the_spare_probe(self):
        """[EC] TT5b takes over, and gives the job back only when the brewer says."""
        sim = fermentation()
        plant = InProcessPlant(sim)

        await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT5a"))
        await plant.advance(10)

        state = await plant.snapshot()
        assert state.regulation[Vessel.FERM].probe == "TT5b"
        assert (AlarmCode.CONTROL_PROBE_FAULT, Vessel.FERM) in alarms(state)
        assert (await plant.set_temperature(Vessel.FERM, 19)).accepted

        await plant.advance(6 * HOUR)
        assert 18.5 < sim.process.vessels[Vessel.FERM].temp_c < 20.0

        await plant.clear_faults()
        await plant.advance(10)
        assert (await plant.snapshot()).regulation[Vessel.FERM].probe == "TT5b"

        await plant.reset()
        await plant.advance(10)
        state = await plant.snapshot()
        assert state.regulation[Vessel.FERM].probe == "TT5a"
        assert state.alarms == ()

    async def test_pt100_out_of_calibration(self):
        """[EC] Nothing looks wrong: the fermenter just holds the wrong temperature."""
        sim = fermentation()
        plant = InProcessPlant(sim)

        await plant.inject_fault(
            Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
        )
        await plant.advance(HOUR)

        state = await plant.snapshot()
        assert state.alarms == ()
        assert state.readings["TT5a"].quality is Quality.GOOD
        apart = state.readings["TT5a"].value - state.readings["TT5b"].value
        assert apart == pytest.approx(2.0, abs=0.6)
        assert sim.process.vessels[Vessel.FERM].temp_c < 18.0  # the setpoint is 19

    async def test_signal_cable_broken(self, plant):
        """[EC] 0 mA: "no signal", which is not what a faulty instrument sends."""
        await plant.inject_fault(
            Fault(kind=FaultKind.SIGNAL_CABLE_BROKEN, target="TT2")
        )
        await plant.advance(1)

        state = await plant.snapshot()
        reading = state.readings["TT2"]
        assert (reading.quality, reading.value) == (Quality.BAD, None)
        assert (reading.current_ma, reading.reason) == (0.0, "segnale assente")
        assert alarms(state) == {(AlarmCode.SIGNAL_FAULT, "TT2")}

    async def test_signal_cable_broken_on_a_level_means_level_unknown(self, plant):
        """[EC] Interlock 9: with no level, no heating and no transfer."""
        await plant.set_temperature(Vessel.HLT, 72)
        await plant.activate_route(Route.HLT_TO_BOIL, 10)
        await plant.advance(5)

        await plant.inject_fault(
            Fault(kind=FaultKind.SIGNAL_CABLE_BROKEN, target="LT1")
        )
        await plant.advance(1)

        state = await plant.snapshot()
        assert state.devices.heaters["R1"].commanded_pct == 0
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert alarms(state) == {
            (AlarmCode.SIGNAL_FAULT, "LT1"),
            (AlarmCode.HEATER_BLOCKED, "R1"),
            (AlarmCode.TRANSFER_STOPPED, Route.HLT_TO_BOIL),
        }
        transfer = await plant.activate_route(Route.HLT_TO_MASH, 5)
        heating = await plant.set_temperature(Vessel.HLT, 70)
        assert transfer.code is CommandCode.LEVEL_UNKNOWN
        assert heating.code is CommandCode.LEVEL_UNKNOWN

    async def test_level_stuck_fools_the_controller_and_k1_trips(self, sim, plant):
        """[EC] The example of docs/impianto.md, and the test of K1.

        The level says 20 L in an empty kettle: the controller lets the
        element work dry. The true temperature rises and the thermostat,
        which is wired and reads no signal, opens K1.
        """
        await plant.inject_fault(
            Fault(kind=FaultKind.LEVEL_STUCK, target="LT3", value=20.0)
        )
        await plant.advance(1)
        assert (await plant.set_temperature(Vessel.BOIL, 100)).accepted

        await plant.advance(120)

        state = await plant.snapshot()
        level = state.readings["LT3"]
        assert (level.quality, level.value) == (Quality.GOOD, pytest.approx(20, 0.01))
        assert not state.devices.safety_contactor.closed
        assert (AlarmCode.SAFETY_OPEN, "K1") in alarms(state)
        assert sim.process.vessels[Vessel.BOIL].liquid_l == 0

    async def test_level_disturbed_by_foam(self, sim, plant):
        """[EC] Now and then a jump upwards, with good quality (SICK manual, 11.4)."""
        sim.process.vessels[Vessel.BOIL].liquid_l = 20.0
        await plant.inject_fault(Fault(kind=FaultKind.LEVEL_FOAM, target="LT3"))
        readings = []

        for _ in range(600):
            await plant.advance(1)
            readings.append((await plant.snapshot()).readings["LT3"])

        values = [reading.value for reading in readings]
        assert all(reading.quality is Quality.GOOD for reading in readings)
        assert 5 < sum(value > 21 for value in values) < 100
        assert median(values) == pytest.approx(20, abs=0.7)

    async def test_hydrometer_battery_low(self):
        """[EC] The voltage falls message after message, then silence."""
        plant = InProcessPlant(fermentation())
        fresh = (await plant.snapshot()).readings["DT1.battery"].value

        await plant.inject_fault(
            Fault(kind=FaultKind.HYDROMETER_BATTERY_LOW, target="DT1")
        )
        await plant.advance(2 * HOUR)

        state = await plant.snapshot()
        assert state.readings["DT1.battery"].value < fresh - 0.1
        assert state.readings["DT1"].quality is Quality.GOOD

        await plant.advance(8 * HOUR)

        state = await plant.snapshot()
        assert state.readings["DT1"].quality is Quality.STALE
        assert (AlarmCode.HYDROMETER_SILENT, "DT1") in alarms(state)

    async def test_hydrometer_wifi_lost(self):
        """[EC] Silence at once, with the battery still good."""
        plant = InProcessPlant(fermentation())

        await plant.inject_fault(
            Fault(kind=FaultKind.HYDROMETER_WIFI_LOST, target="DT1")
        )
        await plant.advance(40 * 60)

        state = await plant.snapshot()
        gravity = state.readings["DT1"]
        assert gravity.quality is Quality.STALE
        assert gravity.value == pytest.approx(1.050, abs=0.003)  # the last one sent
        assert gravity.sim_time_s == 0
        assert state.readings["DT1.battery"].value >= 4.0
        assert alarms(state) == {(AlarmCode.HYDROMETER_SILENT, "DT1")}

        # This alarm stops nothing, so it ends with its cause
        await plant.clear_faults()
        await plant.advance(15 * 60)
        assert (await plant.snapshot()).alarms == ()


class TestProcessFaults:
    async def test_pump_blocked(self, sim, plant):
        """[EC] Interlock 6: the pump is commanded on, and the level does not move."""
        await plant.inject_fault(Fault(kind=FaultKind.PUMP_BLOCKED, target="P1"))
        assert (await plant.activate_route(Route.HLT_TO_MASH, 13.5)).accepted

        await plant.advance(30)
        assert (await plant.snapshot()).devices.pumps["P1"].commanded_on

        await plant.advance(60)

        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert alarms(state) == {(AlarmCode.TRANSFER_NO_PROGRESS, Route.HLT_TO_MASH)}
        assert sim.process.vessels[Vessel.MASH].liquid_l == 0

        # A new transfer takes the place of the one that ended badly
        await plant.clear_faults()
        assert (await plant.activate_route(Route.HLT_TO_MASH, 13.5)).accepted
        assert (await plant.snapshot()).alarms == ()
        await plant.advance(120)
        assert sim.process.vessels[Vessel.MASH].liquid_l == pytest.approx(13.5, abs=0.3)

    async def test_valve_stuck(self, sim, plant):
        """[EC] Interlock 7: no end contact in 10 s, and the pump never starts."""
        await plant.inject_fault(Fault(kind=FaultKind.VALVE_STUCK, target="EV2a"))
        assert (await plant.activate_route(Route.HLT_TO_MASH, 13.5)).accepted

        await plant.advance(5)
        state = await plant.snapshot()
        valve = state.devices.valves["EV2a"]
        assert (valve.commanded_open, valve.open_contact) == (True, False)
        assert not state.devices.pumps["P1"].commanded_on

        await plant.advance(10)

        state = await plant.snapshot()
        assert state.transfer is None
        assert alarms(state) == {(AlarmCode.VALVE_NOT_REACHED, "EV2a")}
        assert sim.process.vessels[Vessel.MASH].liquid_l == 0

        # The alarm of a transfer that ended badly stays until the brewer sees it
        await plant.advance(60)
        assert (AlarmCode.VALVE_NOT_REACHED, "EV2a") in alarms(await plant.snapshot())
        await plant.reset()
        await plant.advance(1)
        assert (await plant.snapshot()).alarms == ()

    async def test_valve_stuck_open(self, sim, mashed):
        """[EC] Interlock 7 on the way back: the valve does not close.

        Stuck means it stays where it is. The alarm outlives the next
        transfer, because its cause does; and the pump now has two ways
        open, so half of its flow goes round the tun.
        """
        await mashed.activate_route(Route.MASH_RECIRC)
        await mashed.advance(5)
        await mashed.inject_fault(Fault(kind=FaultKind.VALVE_STUCK, target="EV5"))

        await mashed.stop_route()
        await mashed.advance(10)

        state = await mashed.snapshot()
        valve = state.devices.valves["EV5"]
        assert (valve.commanded_open, valve.open_contact) == (False, True)
        assert alarms(state) == {(AlarmCode.VALVE_NOT_REACHED, "EV5")}

        assert (await mashed.activate_route(Route.MASH_TO_BOIL, 5)).accepted
        await mashed.advance(31)

        assert alarms(await mashed.snapshot()) == {(AlarmCode.VALVE_NOT_REACHED, "EV5")}
        kettle = sim.process.vessels[Vessel.BOIL]
        assert kettle.liquid_l == pytest.approx(2.5, abs=0.2)  # 5 L with one way

    async def test_relay_shorted_on_the_hlt_trips_k1(self, sim, plant):
        """[EC] Commanded at 0 %, and heating: at 90 °C the thermostat opens K1.

        K1 closes again only with reset, and only below the limit.
        """
        hlt = sim.process.vessels[Vessel.HLT]
        hlt.temp_c = 88.0
        await plant.inject_fault(Fault(kind=FaultKind.SSR_SHORTED, target="R1"))

        await plant.advance(300)

        state = await plant.snapshot()
        assert state.devices.heaters["R1"].commanded_pct == 0
        assert not state.devices.safety_contactor.closed
        assert alarms(state) == {(AlarmCode.SAFETY_OPEN, "K1")}

        hlt.temp_c = 95.0
        assert (await plant.reset()).accepted  # the controller cannot know better
        await plant.advance(1)
        assert not (await plant.snapshot()).devices.safety_contactor.closed

        await plant.clear_faults()
        hlt.temp_c = 80.0
        await plant.advance(5)
        assert not (await plant.snapshot()).devices.safety_contactor.closed  # no reset
        await plant.reset()
        await plant.advance(1)
        state = await plant.snapshot()
        assert state.devices.safety_contactor.closed
        assert state.alarms == ()

    async def test_relay_shorted_on_the_kettle_boils_with_no_command(self, sim, plant):
        """[EC] Water does not pass 100 °C, so K1 stays closed: the level falls."""
        kettle = sim.process.vessels[Vessel.BOIL]
        kettle.liquid_l, kettle.temp_c = 26.0, 99.0
        await plant.inject_fault(Fault(kind=FaultKind.SSR_SHORTED, target="R3"))

        await plant.advance(HOUR // 2)

        state = await plant.snapshot()
        assert state.devices.heaters["R3"].commanded_pct == 0
        assert state.devices.safety_contactor.closed
        assert state.readings["TT3"].value == pytest.approx(100, abs=0.5)
        assert kettle.liquid_l < 25.0

    async def test_relay_shorted_on_the_fermenter_keeps_the_glycol_open(self):
        """[EC] The glycol makes up for it: EV9 is open far more than usual.

        WHY the history holds the mean of a command over each minute: EV9
        opens for a couple of minutes at a time, and a sample of the
        instant would miss most of them.
        """
        plant = InProcessPlant(fermentation())
        await plant.advance(4 * HOUR)
        usual = mean(sample.value for sample in await plant.history("EV9"))

        await plant.inject_fault(Fault(kind=FaultKind.SSR_SHORTED, target="R4"))
        await plant.advance(6 * HOUR)

        state = await plant.snapshot()
        since_fault = await plant.history("EV9", since_s=4 * HOUR)
        assert usual < 5
        assert mean(sample.value for sample in since_fault) > 20
        assert state.devices.heaters["R4"].commanded_pct == 0
        assert state.alarms == ()

    async def test_heater_element_open(self, sim, plant):
        """[EC] Commanded at 100 %, and the temperature does not move."""
        await plant.inject_fault(Fault(kind=FaultKind.HEATER_OPEN, target="R1"))
        await plant.set_temperature(Vessel.HLT, 72)

        await plant.advance(600)

        state = await plant.snapshot()
        assert state.devices.heaters["R1"].commanded_pct == 100
        assert state.alarms == ()
        assert sim.process.vessels[Vessel.HLT].temp_c == pytest.approx(20, abs=0.1)

    async def test_glycol_failed(self):
        """[EC] EV9 is open and its contact agrees, yet the temperature rises."""
        sim = fermentation(progress=0.5, room_c=25.0)
        plant = InProcessPlant(sim)

        await plant.inject_fault(Fault(kind=FaultKind.GLYCOL_FAILED, target="CHILLER"))
        await plant.advance(3 * HOUR)

        state = await plant.snapshot()
        valve = state.devices.valves["EV9"]
        assert (valve.commanded_open, valve.open_contact) == (True, True)
        assert state.alarms == ()
        assert sim.process.vessels[Vessel.FERM].temp_c > 20.0  # the setpoint is 19

    async def test_drive_fault(self, mashed):
        """[EC] The drive gives its code; no agitator, so no heating in the tun.

        The fault stays until reset, and one reset is enough for the chain:
        drive, agitator, heater.
        """
        await mashed.set_agitator(True)
        await mashed.advance(1)
        await mashed.set_temperature(Vessel.MASH, 66)
        await mashed.advance(1)

        await mashed.inject_fault(
            Fault(kind=FaultKind.DRIVE_FAULT, target="M1", value=11)
        )
        await mashed.advance(1)

        state = await mashed.snapshot()
        drive = state.devices.agitator
        assert (drive.commanded_run, drive.running, drive.fault_code) == (
            True,
            False,
            11,
        )
        assert alarms(state) == {
            (AlarmCode.DRIVE_FAULT, "M1"),
            (AlarmCode.HEATER_BLOCKED, "R2"),
        }
        assert any("F11" in alarm.text for alarm in state.alarms)
        assert state.devices.heaters["R2"].commanded_pct == 0
        assert (await mashed.set_agitator(True)).code is CommandCode.DRIVE_FAULT

        await mashed.clear_faults()
        await mashed.advance(5)
        assert (await mashed.snapshot()).devices.agitator.fault_code == 11

        await mashed.reset()
        await mashed.advance(1)

        state = await mashed.snapshot()
        assert state.devices.agitator.running
        assert state.devices.heaters["R2"].commanded_pct == 100
        assert state.alarms == ()

    async def test_fermentation_stuck(self):
        """[EC] The gravity stops well above 1.010, and nothing else changes."""
        plant = InProcessPlant(fermentation(progress=0.3))
        await plant.inject_fault(
            Fault(kind=FaultKind.FERMENTATION_STUCK, target=Vessel.FERM)
        )
        before = (await plant.snapshot()).readings["DT1"].value

        await plant.advance(24 * HOUR)

        state = await plant.snapshot()
        gravity = state.readings["DT1"]
        assert gravity.quality is Quality.GOOD
        assert gravity.value == pytest.approx(before, abs=0.002)
        assert gravity.value > 1.030
        assert state.alarms == ()


class TestFaultsThatDoNotExist:
    @pytest.mark.parametrize(
        ("kind", "target", "value"),
        [
            (FaultKind.PUMP_BLOCKED, "TT1", None),  # a probe is not a pump
            (FaultKind.VALVE_STUCK, "EV1", None),  # no such valve
            (FaultKind.PROBE_OFFSET, "TT1", None),  # by how much?
            (FaultKind.PUMP_BLOCKED, "P1", 3.0),  # a number that means nothing
        ],
    )
    async def test_a_fault_the_plant_does_not_admit_is_an_error(
        self, plant, kind, target, value
    ):
        """[EC] Refused, and the plant stays healthy.

        WHY: the prototype accepted a fault on a tag that could not have
        it and did nothing: the scenario ran healthy, and looked passed.
        """
        with pytest.raises(ValidationError):
            await plant.inject_fault(Fault(kind=kind, target=target, value=value))

        await plant.activate_route(Route.HLT_TO_MASH, 5)
        await plant.advance(60)
        state = await plant.snapshot()
        assert state.alarms == ()
        assert state.readings["LT2"].value == pytest.approx(8, abs=0.7)
