"""Tests for the read-only wrapper of the plant.

Under test: src/neuralbrewery/core/plant/readonly.py, around the in-process
plant

WHY these tests exist: rule 1 of AGENTS.md, no agent receives
PlantCommander. The in-process plant is all three ports at once, so an
agent typed as PlantReader could still press a button at run time. The
wrapper must read as the plant does, and command nothing.
"""

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.plant.protocols import (
    PlantCommander,
    PlantReader,
    SimulationControl,
)
from neuralbrewery.core.plant.readonly import ReadOnlyPlant
from neuralbrewery.core.plant.schemas import Route


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
