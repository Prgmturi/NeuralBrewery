"""Tests for the brew program of the controller.

Under test: src/neuralbrewery/adapters/plant_sim/controller/ (program.py, and
the program in controller.py), through the ports
Spec: docs/impianto.md, "Programma della cotta", and check 6 of "Controlli
di plausibilità".

WHY these tests exist: the program runs the brew day of the evals and of
the demo. A diagnosis starts from where the program is and from why it
stopped; and after a block nothing may start again until the brewer says
so, the program included.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.plant.schemas import (
    AlarmCode,
    CommandCode,
    EventKind,
    Fault,
    FaultKind,
    PlantState,
    Program,
    ProgramStatus,
    Quality,
    Route,
    Vessel,
)
from tests.adapters.plant_sim.conftest import alarms

HOUR = 3600
HOT_SIDE = (Vessel.HLT, Vessel.MASH, Vessel.BOIL)
STEPS = [
    "Scalda l'acqua",
    "Impasto",
    "Porta il tino a 66 °C",
    "Sosta",
    "Fine sosta",
    "Ricircolo",
    "Primo mosto",
    "Lavaggio",
    "Ricircolo",
    "Secondo mosto",
    "Porta a bollore",
    "Bollitura",
    "Pronto al travaso",
    "Al fermentatore",
    "Lievito",
]
PAUSED_ALARM = (AlarmCode.PROGRAM_PAUSED, "PROGRAM")


async def follow(
    plant: InProcessPlant, *, to_step: int = 0, pace_s: int = 1
) -> Program:
    """Let the program run, confirming where it waits, up to that step.

    With no step, up to the end. The program must get there on its own
    legs: a pause on the way fails the test.
    """
    for _ in range(0, 5 * HOUR, pace_s):
        program = (await plant.snapshot()).program
        if program.step == to_step or program.status is ProgramStatus.DONE:
            return program
        if program.status is ProgramStatus.WAITING:
            assert (await plant.confirm_step()).accepted
        else:
            assert program.status is ProgramStatus.RUNNING, program
            await plant.advance(pace_s)
    raise AssertionError(f"step {to_step} not reached in 5 hours")


def hot_setpoints(state: PlantState) -> list[float | None]:
    """The setpoints of HLT, tun and kettle, in this order."""
    return [state.regulation[vessel].setpoint_c for vessel in HOT_SIDE]


@pytest.fixture
async def brewing(sim, plant) -> InProcessPlant:
    """The program started with the water already hot.

    Heating 35 L takes 45 simulated minutes, which most tests do not need.
    """
    sim.process.vessels[Vessel.HLT].temp_c = 72.0
    assert (await plant.start_program()).accepted
    return plant


class TestWholeBatch:
    async def test_a_whole_batch_puts_20_litres_in_the_fermenter(self, sim, plant):
        """[HP] Check 6: from cold water to pitched wort, with no alarm.

        The brewer confirms twice: before the wort leaves the kettle, and
        when the yeast goes in. Without the first confirm the program waits.
        """
        assert (await plant.start_program()).accepted

        await follow(plant, to_step=13, pace_s=5)
        boiled_at_s = (await plant.snapshot()).sim_time_s
        await plant.advance(600)
        waiting = (await plant.snapshot()).program
        assert (waiting.status, waiting.step) == (ProgramStatus.WAITING, 13)
        done = await follow(plant, pace_s=5)

        assert (done.status, done.step) == (ProgramStatus.DONE, 15)
        assert 3.4 * HOUR < boiled_at_s < 3.8 * HOUR  # the whole batch: 3 h 40 min
        events = await plant.events()
        begun = [event.text for event in events if event.kind is EventKind.PROGRAM_STEP]
        assert begun == [f"passo {n} ({name})" for n, name in enumerate(STEPS, 1)]
        assert events[-1].kind is EventKind.PROGRAM_DONE
        assert not [event for event in events if event.kind is EventKind.ALARM_RAISED]

        vessels = sim.process.vessels
        assert vessels[Vessel.FERM].liquid_l == pytest.approx(20, abs=0.5)
        assert vessels[Vessel.BOIL].liquid_l > 3.0  # the pump never ran dry
        state = await plant.snapshot()
        assert state.transfer is None
        assert not state.devices.agitator.commanded_run
        assert hot_setpoints(state) == [None, None, None]
        assert state.regulation[Vessel.FERM].setpoint_c == 19

        # The last confirm was the pitch: the yeast works, the hydrometer speaks
        assert sim.process.fermentation.activity is not None
        await plant.advance(HOUR)
        gravity = (await plant.snapshot()).readings["DT1"]
        assert gravity.quality is Quality.GOOD
        assert gravity.value == pytest.approx(1.050, abs=0.003)

    async def test_same_seed_same_batch(self):
        """[HP] Two runs of the program end in the same plant, to the last digit."""

        async def batch():
            plant = InProcessPlant(brew_day(seed=7))
            await plant.start_program()
            await follow(plant, pace_s=10)
            return await plant.snapshot(), await plant.events()

        assert await batch() == await batch()


class TestSteps:
    async def test_the_snapshot_says_where_the_program_is(self, plant):
        """[HP] Status, step, time spent in the step and its longest time."""
        assert (await plant.snapshot()).program == Program(status=ProgramStatus.IDLE)

        assert (await plant.start_program()).accepted
        await plant.advance(61)

        state = await plant.snapshot()
        assert state.program == Program(
            status=ProgramStatus.RUNNING,
            step=1,
            step_name="Scalda l'acqua",
            elapsed_s=60,  # the first second went in giving the commands
            max_s=HOUR,
        )
        assert state.regulation[Vessel.HLT].setpoint_c == 72
        assert state.devices.heaters["R1"].commanded_pct == 100

    async def test_the_program_presses_the_buttons_of_the_brewer(self, brewing):
        """[HP] Its commands are events like any other, and each is given once.

        WHY: a command already in place is not given again. A step that
        repeated its setpoints would re-arm what an interlock had stopped,
        and fill the events an agent reads with commands nobody decided.
        """
        await follow(brewing, to_step=7, pace_s=5)
        await brewing.advance(2)

        commands = [
            (event.code, event.tag, event.text)
            for event in await brewing.events()
            if event.kind is EventKind.COMMAND
        ]
        assert commands == [
            ("start_program", "PROGRAM", "cotta di riferimento"),
            ("set_temperature", Vessel.HLT, "72 °C"),  # step 1
            ("activate_route", Route.HLT_TO_MASH, "13.5 L"),  # step 2
            ("set_agitator", "M1", "acceso"),  # step 3
            ("set_temperature", Vessel.HLT, "78 °C"),
            ("set_temperature", Vessel.MASH, "66 °C"),
            ("set_temperature", Vessel.MASH, "76 °C"),  # step 4 changes nothing; 5
            ("activate_route", Route.MASH_RECIRC, "ricircolo"),  # step 6
            ("set_agitator", "M1", "spento"),
            ("set_temperature", Vessel.MASH, "spento"),  # step 7
            ("stop_route", Route.MASH_RECIRC, "fermato a 0.0 L"),
            ("activate_route", Route.MASH_TO_BOIL, "9 L"),
        ]

    async def test_a_step_past_its_time_is_late_and_goes_on(self, plant):
        """[EC] The element of R1 is open: an hour on, the water is still cold.

        step_late only warns. The step is neither skipped nor stopped: the
        element is repaired, the water heats, and the alarm ends with the step.
        """
        await plant.inject_fault(Fault(kind=FaultKind.HEATER_OPEN, target="R1"))
        await plant.start_program()
        await plant.advance(HOUR)
        assert (await plant.snapshot()).alarms == ()

        await plant.advance(120)

        state = await plant.snapshot()
        assert alarms(state) == {(AlarmCode.STEP_LATE, "PROGRAM")}
        assert "60 min" in state.alarms[0].text
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 1)

        await plant.clear_faults()
        await follow(plant, to_step=2, pace_s=10)
        assert (await plant.snapshot()).alarms == ()


class TestAutomaticPause:
    async def test_a_blocked_pump_pauses_the_mash_in(self, sim, brewing):
        """[EC] The level stops moving: the transfer ends in alarm, the program waits.

        WHY: the controller never restarts by itself, and the program is the
        controller. After a block it goes on only with reset and resume; and
        then it moves the litres still missing, not the whole quantity again.
        """
        await follow(brewing, to_step=2)
        await brewing.advance(30)
        await brewing.inject_fault(Fault(kind=FaultKind.PUMP_BLOCKED, target="P1"))
        await brewing.advance(150)  # interlock 6 takes one to two minutes

        state = await brewing.snapshot()
        paused = state.program
        assert (paused.status, paused.step) == (ProgramStatus.PAUSED, 2)
        assert "livello di HLT fermo" in paused.reason
        assert alarms(state) == {
            (AlarmCode.TRANSFER_NO_PROGRESS, Route.HLT_TO_MASH),
            PAUSED_ALARM,
        }
        assert state.regulation[Vessel.HLT].setpoint_c == 72  # temperatures stay
        assert 3 < sim.process.vessels[Vessel.MASH].liquid_l < 6

        await brewing.advance(300)
        assert (await brewing.snapshot()).program == paused  # the clock too
        refused = await brewing.resume_program()
        assert (refused.accepted, refused.code) == (False, CommandCode.ALARM_ACTIVE)

        await brewing.clear_faults()
        assert (await brewing.reset()).accepted
        assert (await brewing.resume_program()).accepted  # one right after the other
        await follow(brewing, to_step=3)

        assert (await brewing.snapshot()).alarms == ()
        tun = sim.process.vessels[Vessel.MASH]
        assert tun.liquid_l == pytest.approx(13.5, abs=0.5)

    async def test_a_drive_fault_pauses_the_mash_rest(self, brewing):
        """[EC] No agitator, so no heating in the tun, so the program holds."""
        await follow(brewing, to_step=4)
        await brewing.advance(60)
        await brewing.inject_fault(
            Fault(kind=FaultKind.DRIVE_FAULT, target="M1", value=11)
        )
        await brewing.advance(2)

        state = await brewing.snapshot()
        paused = state.program
        assert (paused.status, paused.step) == (ProgramStatus.PAUSED, 4)
        assert "F11" in paused.reason
        assert alarms(state) == {
            (AlarmCode.DRIVE_FAULT, "M1"),
            (AlarmCode.HEATER_BLOCKED, "R2"),
            PAUSED_ALARM,
        }
        assert state.regulation[Vessel.HLT].setpoint_c == 78

        await brewing.clear_faults()
        await brewing.reset()
        await brewing.resume_program()
        await brewing.advance(10)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 4)
        assert state.program.elapsed_s > paused.elapsed_s  # the rest is not begun again
        assert state.devices.agitator.running
        assert state.alarms == ()

    async def test_k1_open_pauses_the_program_until_it_closes(self, sim, plant):
        """[EC] The controller cannot close K1, nor know whether reset will.

        So a resume right after reset is let go, and the program pauses
        again when K1 turns out to be still open.
        """
        await plant.start_program()
        await plant.advance(60)
        hlt = sim.process.vessels[Vessel.HLT]
        hlt.temp_c = 91.0  # over its thermostat
        await plant.advance(1)

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.PAUSED
        assert "K1" in state.program.reason
        assert alarms(state) == {(AlarmCode.SAFETY_OPEN, "K1"), PAUSED_ALARM}

        await plant.reset()
        assert (await plant.resume_program()).accepted
        await plant.advance(1)
        assert (await plant.snapshot()).program.status is ProgramStatus.PAUSED

        hlt.temp_c = 60.0
        await plant.reset()
        await plant.resume_program()
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.RUNNING
        assert state.alarms == ()

    async def test_a_broken_control_probe_pauses_the_program(self, plant):
        """[EC] TT1 breaks while the water heats: no regulation, no step."""
        await plant.start_program()
        await plant.advance(60)

        await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT1"))
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.PAUSED
        assert "TT1" in state.program.reason
        assert alarms(state) == {
            (AlarmCode.SIGNAL_FAULT, "TT1"),
            (AlarmCode.CONTROL_PROBE_FAULT, Vessel.HLT),
            PAUSED_ALARM,
        }

    async def test_a_command_the_plant_refuses_pauses_the_program(self, brewing):
        """[EC] The level of the tun is stuck low: step 3 cannot start the agitator.

        The program is answered as a brewer would be. Nothing is blocked,
        so there is nothing to reset: resume is accepted, and the plant
        refuses again until the cause is gone.
        """
        await brewing.inject_fault(
            Fault(kind=FaultKind.LEVEL_STUCK, target="LT2", value=5.0)
        )
        await follow(brewing, to_step=3)
        await brewing.advance(2)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.PAUSED, 3)
        assert "LT2 sotto 8 L" in state.program.reason
        assert alarms(state) == {PAUSED_ALARM}

        assert (await brewing.resume_program()).accepted
        await brewing.advance(2)
        assert (await brewing.snapshot()).program.status is ProgramStatus.PAUSED

        await brewing.clear_faults()
        await brewing.advance(1)
        await brewing.resume_program()
        await brewing.advance(2)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 3)
        assert state.devices.agitator.running
        assert state.regulation[Vessel.MASH].setpoint_c == 66
        assert state.alarms == ()


class TestBrewerPause:
    async def test_pause_holds_the_step_and_resume_takes_it_up(self, sim, brewing):
        """[HP] Temperatures stay, the transfer and the clock stop. No alarm."""
        tun = sim.process.vessels[Vessel.MASH]
        await follow(brewing, to_step=2)
        await brewing.advance(30)

        assert (await brewing.pause_program()).accepted
        await brewing.advance(2)

        paused = await brewing.snapshot()
        in_the_tun = tun.liquid_l
        assert paused.program.status is ProgramStatus.PAUSED
        assert paused.program.elapsed_s == pytest.approx(30, abs=2)  # kept
        assert paused.transfer is None
        assert not paused.devices.pumps["P1"].commanded_on
        assert paused.regulation[Vessel.HLT].setpoint_c == 72
        assert 3 < in_the_tun < 6

        await brewing.advance(600)
        state = await brewing.snapshot()
        assert state.program == paused.program
        assert tun.liquid_l == in_the_tun
        assert state.alarms == ()  # the brewer asked: not an alarm, and not late

        assert (await brewing.resume_program()).accepted
        await follow(brewing, to_step=3)
        assert tun.liquid_l == pytest.approx(13.5, abs=0.5)

    async def test_a_pause_in_the_second_a_transfer_ends_moves_no_more(
        self, sim, brewing
    ):
        """[EC] The mash-in has just moved its last litre when the brewer pauses.

        WHY: the step was not closed yet. On resume nothing was left to
        move: the program asked the plant for "-0.1 L", was refused, and
        paused for good.
        """
        tun = sim.process.vessels[Vessel.MASH]
        await follow(brewing, to_step=2)
        await brewing.advance(5)
        while (await brewing.snapshot()).transfer is not None:
            await brewing.advance(1)
        in_the_tun = tun.liquid_l

        assert (await brewing.pause_program()).accepted
        assert (await brewing.snapshot()).program.step == 2
        assert (await brewing.resume_program()).accepted
        await brewing.advance(5)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 3)
        assert tun.liquid_l == in_the_tun
        assert state.alarms == ()

    async def test_the_recirculation_goes_on_through_a_pause(self, brewing):
        """[EC] Paused while the tun is heated through the recirculation.

        WHY: with the pump stopped the wort would stand still, the heater
        would be blocked, and a pause the brewer asked for would end in an
        alarm and a tun getting cold.
        """
        await follow(brewing, to_step=6, pace_s=5)
        await brewing.advance(30)

        await brewing.pause_program()
        await brewing.advance(300)

        state = await brewing.snapshot()
        assert state.program.status is ProgramStatus.PAUSED
        assert state.transfer.route is Route.MASH_RECIRC
        assert state.devices.pumps["P2"].commanded_on
        assert state.regulation[Vessel.MASH].setpoint_c == 76
        assert state.readings["TT2"].value == pytest.approx(76, abs=1)
        assert state.alarms == ()

        await brewing.resume_program()
        await brewing.advance(5)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 6)
        assert state.devices.pumps["P2"].commanded_on
        assert state.alarms == ()


class TestManualCommands:
    async def test_the_hot_side_is_the_programs_while_it_runs(self, sim, plant):
        """[EC] A manual command that starts something is refused.

        The fermenter is not the program's: yesterday's beer is in there.
        """
        sim.process.vessels[Vessel.FERM].liquid_l = 20.0
        await plant.advance(1)
        await plant.start_program()
        await plant.advance(10)

        for refused in (
            await plant.set_temperature(Vessel.HLT, 80),
            await plant.activate_route(Route.HLT_TO_BOIL, 5),
            await plant.set_agitator(True),
        ):
            assert (refused.accepted, refused.code) == (
                False,
                CommandCode.PROGRAM_RUNNING,
            )
        assert (await plant.set_temperature(Vessel.FERM, 18)).accepted

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.RUNNING
        assert state.regulation[Vessel.HLT].setpoint_c == 72
        assert state.regulation[Vessel.FERM].setpoint_c == 18

    async def test_a_manual_stop_is_obeyed_and_pauses_the_program(self, plant):
        """[EC] A stop is never refused; the program steps aside, with no alarm.

        In pause the hot side is the brewer's. Resume puts the step back.
        """
        await plant.start_program()
        await plant.advance(10)

        assert (await plant.set_temperature(Vessel.HLT, None)).accepted

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.PAUSED
        assert state.regulation[Vessel.HLT].setpoint_c is None
        assert state.alarms == ()
        assert (await plant.set_temperature(Vessel.HLT, 60)).accepted

        assert (await plant.resume_program()).accepted
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.RUNNING
        assert state.regulation[Vessel.HLT].setpoint_c == 72

    async def test_stop_all_pauses_and_resume_puts_the_step_back(self, brewing):
        """[EC] Everything off in the mash rest; then agitator and heat again.

        The step states the whole hot side, so nothing is lost. And the tun
        is heated in the same scan the agitator is asked to start: interlock
        2 goes by the command.
        """
        await follow(brewing, to_step=4)
        await brewing.advance(10)

        assert (await brewing.stop_all()).accepted
        await brewing.advance(5)

        state = await brewing.snapshot()
        assert state.program.status is ProgramStatus.PAUSED
        assert hot_setpoints(state) == [None, None, None]
        assert not state.devices.agitator.running
        assert state.alarms == ()

        assert (await brewing.resume_program()).accepted
        await brewing.advance(3)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.RUNNING, 4)
        assert hot_setpoints(state) == [78, 66, None]
        assert state.devices.agitator.running
        assert state.alarms == ()

    async def test_abort_closes_the_program_and_leaves_the_fermenter(
        self, sim, brewing
    ):
        """[EC] The hot side stops for good; a new program may start."""
        sim.process.vessels[Vessel.FERM].liquid_l = 20.0
        await brewing.advance(1)
        assert (await brewing.set_temperature(Vessel.FERM, 19)).accepted
        await follow(brewing, to_step=2)
        await brewing.advance(20)

        assert (await brewing.abort_program()).accepted
        await brewing.advance(2)

        state = await brewing.snapshot()
        assert (state.program.status, state.program.step) == (ProgramStatus.ABORTED, 2)
        assert state.transfer is None
        assert not state.devices.pumps["P1"].commanded_on
        assert state.regulation[Vessel.HLT].setpoint_c is None
        assert state.regulation[Vessel.FERM].setpoint_c == 19
        assert state.alarms == ()
        assert (await brewing.resume_program()).code is CommandCode.PROGRAM_STATE

        assert (await brewing.start_program()).accepted
        assert (await brewing.snapshot()).program.step == 1


class TestCommandsOutOfPlace:
    async def test_a_program_command_needs_the_program_in_the_right_state(self, plant):
        """[EC] Refused with the reason. The two that stop are always accepted."""
        assert (await plant.confirm_step()).code is CommandCode.PROGRAM_STATE
        assert (await plant.resume_program()).code is CommandCode.PROGRAM_STATE
        assert (await plant.pause_program()).accepted
        assert (await plant.abort_program()).accepted
        assert (await plant.snapshot()).program.status is ProgramStatus.IDLE

        assert (await plant.start_program()).accepted
        await plant.advance(5)
        assert (await plant.start_program()).code is CommandCode.PROGRAM_STATE
        assert (await plant.confirm_step()).code is CommandCode.PROGRAM_STATE
        assert (await plant.pause_program()).accepted
        assert (await plant.pause_program()).accepted
        assert (await plant.start_program()).code is CommandCode.PROGRAM_STATE

    async def test_the_program_does_not_start_into_a_block(self, sim, plant):
        """[EC] K1 is open: start is refused. Right after reset it is let go."""
        hlt = sim.process.vessels[Vessel.HLT]
        hlt.temp_c = 91.0
        await plant.advance(1)

        refused = await plant.start_program()

        assert (refused.accepted, refused.code) == (False, CommandCode.ALARM_ACTIVE)
        assert "K1" in refused.reason
        assert (await plant.snapshot()).program.status is ProgramStatus.IDLE

        hlt.temp_c = 60.0
        await plant.reset()
        assert (await plant.start_program()).accepted
        await plant.advance(2)

        state = await plant.snapshot()
        assert state.program.status is ProgramStatus.RUNNING
        assert state.alarms == ()
