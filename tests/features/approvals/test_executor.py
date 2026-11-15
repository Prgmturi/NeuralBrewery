"""Tests for the executor: the approved button, pressed on the plant.

Module under test: src/neuralbrewery/features/approvals/api/executor.py
Layer: Edge of the feature, on the in-process plant through its port

WHY these tests exist: the executor is the only code that holds
PlantCommander. What it presses must be the button that was approved,
with its arguments, and the controller's answer must come back whole: a
refusal of an interlock included, which is an answer, not an error.
"""

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.features.approvals.api.executor import Executor
from neuralbrewery.features.approvals.domain.proposal import Action
from neuralbrewery.features.approvals.domain.protocols import Panel


@pytest.fixture
def plant() -> InProcessPlant:
    return InProcessPlant(brew_day())


async def test_a_setpoint_reaches_the_regulation(plant):
    """[HP] set_temperature HLT 70: accepted, and the controller holds 70 °C."""
    answer = await Executor(plant).press(
        Action("set_temperature", {"vessel": "HLT", "celsius": 70.0})
    )

    assert (answer.accepted, answer.code) == (True, "ok")
    assert (await plant.snapshot()).regulation["HLT"].setpoint_c == 70.0


async def test_no_setpoint_switches_the_vessel_off(plant):
    """[HP] set_temperature with no celsius: the regulation is off."""
    executor = Executor(plant)
    await executor.press(Action("set_temperature", {"vessel": "HLT", "celsius": 70}))

    answer = await executor.press(Action("set_temperature", {"vessel": "HLT"}))

    assert answer.accepted
    assert (await plant.snapshot()).regulation["HLT"].setpoint_c is None


async def test_a_transfer_takes_its_litres(plant):
    """[HP] activate_route with litres: the transfer the controller runs."""
    answer = await Executor(plant).press(
        Action("activate_route", {"route": "hlt_to_mash", "liters": 12})
    )

    assert answer.accepted
    transfer = (await plant.snapshot()).transfer
    assert (transfer.route, transfer.requested_l) == ("hlt_to_mash", 12.0)


async def test_a_refusal_of_the_controller_comes_back_whole(plant):
    """[HP] The kettle is empty: refused, with the code and the reason."""
    answer = await Executor(plant).press(
        Action("activate_route", {"route": "boil_to_ferm", "liters": 5})
    )

    assert not answer.accepted
    assert answer.code == "source_low"
    assert answer.reason


async def test_a_button_with_no_arguments(plant):
    """[HP] set_agitator and stop_all, as approved."""
    executor = Executor(plant)

    off = await executor.press(Action("set_agitator", {"on": False}))
    stop = await executor.press(Action("stop_all", {}))

    assert off.accepted and stop.accepted


def test_the_executor_is_the_panel_of_the_domain(plant):
    """[HP] The port the domain presses through."""
    assert isinstance(Executor(plant), Panel)
