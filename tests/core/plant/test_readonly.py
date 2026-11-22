"""Tests for the read-only wrapper of the plant.

Under test: src/neuralbrewery/core/plant/readonly.py, around the in-process
plant

WHY these tests exist: rule 1 of AGENTS.md, no agent receives
PlantCommander. The in-process plant is all three ports at once, so an
agent typed as PlantReader could still press a button at run time. The
wrapper must read as the plant does, and command nothing. SimulationOnly
is the other wrapper, for the routes of the simulation, and a restart must
reach whoever holds the plant already.
"""

from functools import partial

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.plant.protocols import (
    PlantCommander,
    PlantReader,
    SimulationControl,
)
from neuralbrewery.core.plant.readonly import ReadOnlyPlant, SimulationOnly
from neuralbrewery.core.plant.schemas import ProgramStatus, Route
from neuralbrewery.features.approvals.api.executor import Executor
from neuralbrewery.features.approvals.domain.proposal import Action


async def test_reads_what_the_plant_shows():
    """[HP] Snapshot, events and history, as the plant gives them."""
    plant = InProcessPlant(brew_day())
    assert (await plant.activate_route(Route.HLT_TO_MASH, 5)).accepted
    await plant.advance(120)

    readonly = ReadOnlyPlant(plant)

    assert await readonly.snapshot() == await plant.snapshot()
    assert await readonly.events(60) == await plant.events(60)
    assert await readonly.history("LT1", 60) == await plant.history("LT1", 60)
    assert await readonly.events() == await plant.events()
    assert await readonly.history("LT1") == await plant.history("LT1")


def test_is_a_reader_and_nothing_else():
    """[SEC] No command and no hand on the simulation get through."""
    readonly = ReadOnlyPlant(InProcessPlant(brew_day()))

    assert isinstance(readonly, PlantReader)
    assert not isinstance(readonly, PlantCommander)
    assert not isinstance(readonly, SimulationControl)
    assert not hasattr(readonly, "activate_route")


async def test_the_hand_of_a_test_restarts_the_plant():
    """[HP] SimulationOnly passes the restart on: the plant is back at zero."""
    start = partial(brew_day, seed=42)
    plant = InProcessPlant(start(), start=start)
    control = SimulationOnly(plant)
    await control.advance(600)

    await control.restart()

    assert (await plant.snapshot()).sim_time_s == 0
    assert isinstance(control, SimulationControl)
    assert not isinstance(control, PlantReader)
    assert not isinstance(control, PlantCommander)


async def test_who_got_the_plant_before_a_restart_sees_the_new_one():
    """[HP] Reader and executor are wired once, at start: no wiring again.

    WHY: bootstrap.py hands the same object to readers, agent, MCP server
    and executor. A restart that swapped the object would leave them all
    on the old plant.
    """
    start = partial(brew_day, seed=42)
    plant = InProcessPlant(start(), start=start)
    reader = ReadOnlyPlant(plant)
    executor = Executor(plant)
    await plant.advance(600)

    await plant.restart()
    answer = await executor.press(Action("start_program", {}))

    assert answer.accepted
    state = await reader.snapshot()
    assert state.sim_time_s == 0
    assert state.program.status is ProgramStatus.RUNNING
