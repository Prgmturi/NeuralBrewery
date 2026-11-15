"""Tests for the panel of the controller: its buttons and their limits.

Module under test: src/neuralbrewery/core/plant/panel.py, and Proposal in
src/neuralbrewery/core/plant/schemas.py
Layer: Core, no I/O

WHY these tests exist: the queue of approvals checks every proposal
against the panel, in a domain that loads no pydantic, and the executor
presses the button of the same name on PlantCommander. A button, an
argument or a limit that drifted from the port would let a proposal pass
the guardrail and fail at the plant, or block one the plant would take.
"""

import inspect

import pydantic
import pytest

from neuralbrewery.adapters.plant_sim.layout import VESSELS
from neuralbrewery.core.plant.panel import BUTTONS, MAX_SETPOINT_C, Command
from neuralbrewery.core.plant.protocols import PlantCommander
from neuralbrewery.core.plant.schemas import Proposal, Route, Vessel


def parameters(command: Command) -> set[str]:
    """The arguments of the method of PlantCommander that the button presses."""
    method = getattr(PlantCommander, command.value)
    return set(inspect.signature(method).parameters) - {"self"}


class TestButtons:
    def test_every_button_is_a_method_of_the_commander(self):
        """[SEC] The executor knows every button the panel lists, and no other."""
        methods = {
            name
            for name, member in vars(PlantCommander).items()
            if callable(member) and not name.startswith("_")
        }

        assert {command.value for command in Command} == methods
        assert set(BUTTONS) == set(Command)

    @pytest.mark.parametrize("command", list(Command), ids=str)
    def test_a_button_takes_the_arguments_of_its_method(self, command):
        """[HP] What a button needs and may take are the method's parameters."""
        button = BUTTONS[command]

        assert set(button.needs) | set(button.takes) == parameters(command)
        assert not set(button.needs) & set(button.takes)

    def test_every_vessel_has_its_highest_setpoint(self):
        """[HP] The plate of the plant reads the limit here: one number, one place."""
        assert set(MAX_SETPOINT_C) == set(Vessel)
        for vessel, plate in VESSELS.items():
            assert plate.max_setpoint_c == MAX_SETPOINT_C[vessel]


class TestProposal:
    def test_a_button_needs_its_arguments(self):
        """[EC] activate_route with no route is no proposal."""
        with pytest.raises(pydantic.ValidationError, match="route"):
            Proposal(command=Command.ACTIVATE_ROUTE)

    def test_arguments_are_what_the_queue_takes(self):
        """[HP] Names and JSON values of the arguments given, the command apart."""
        proposal = Proposal(
            command=Command.ACTIVATE_ROUTE, route=Route.HLT_TO_MASH, liters=12.5
        )

        assert proposal.arguments() == {"route": "hlt_to_mash", "liters": 12.5}

    def test_a_setpoint_of_none_is_left_out(self):
        """[EC] set_temperature with no celsius switches the vessel off."""
        proposal = Proposal(command=Command.SET_TEMPERATURE, vessel=Vessel.FERM)

        assert proposal.arguments() == {"vessel": "FERM"}
