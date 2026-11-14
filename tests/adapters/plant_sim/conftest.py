"""Fixtures for the tests of the simulated plant.

Every test drives the whole plant through its three ports, as the app will:
commands and readings pass through the controller. The simulator itself is
at hand too, for what only a test may do: look at the true values, and put
the plant in a state by hand.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.simulator import PlantSimulator
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.plant.schemas import AlarmCode, PlantState, Route


@pytest.fixture
def sim() -> PlantSimulator:
    """Brew day: 35 L in the HLT, dry grain in the tun, the rest empty."""
    return brew_day()


@pytest.fixture
def plant(sim: PlantSimulator) -> InProcessPlant:
    return InProcessPlant(sim)


@pytest.fixture
async def mashed(plant: InProcessPlant) -> InProcessPlant:
    """Brew day after the mash-in: 13.5 L of water on the grain, 21.5 L left."""
    assert (await plant.activate_route(Route.HLT_TO_MASH, 13.5)).accepted
    await plant.advance(120)
    return plant


def alarms(state: PlantState) -> set[tuple[AlarmCode, str]]:
    """The active alarms, as (code, tag)."""
    return {(alarm.code, alarm.tag) for alarm in state.alarms}
