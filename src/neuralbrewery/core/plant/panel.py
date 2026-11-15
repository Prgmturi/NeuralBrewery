"""The panel of the controller: vessels, routes, buttons, and their limits.

Plain Python, with no pydantic: the queue of approvals checks every
proposal against the panel in its domain, which loads no framework.
schemas.py takes Vessel, Route and Command from here, so the rest of the
app imports them from either.
"""

from dataclasses import dataclass
from enum import StrEnum


class Vessel(StrEnum):
    HLT = "HLT"  # hot liquor tank: the hot water
    MASH = "MASH"  # mash tun
    BOIL = "BOIL"  # kettle
    FERM = "FERM"  # fermenter


class Route(StrEnum):
    """The only ways liquid may move. No free combination of valves."""

    HLT_TO_MASH = "hlt_to_mash"
    HLT_TO_BOIL = "hlt_to_boil"
    MASH_RECIRC = "mash_recirc"
    MASH_TO_BOIL = "mash_to_boil"
    BOIL_TO_FERM = "boil_to_ferm"


class Command(StrEnum):
    """The buttons of the panel: the methods of the commander port, by name."""

    ACTIVATE_ROUTE = "activate_route"
    STOP_ROUTE = "stop_route"
    SET_TEMPERATURE = "set_temperature"
    SET_AGITATOR = "set_agitator"
    START_PROGRAM = "start_program"
    CONFIRM_STEP = "confirm_step"
    PAUSE_PROGRAM = "pause_program"
    RESUME_PROGRAM = "resume_program"
    ABORT_PROGRAM = "abort_program"
    STOP_ALL = "stop_all"
    RESET = "reset"


@dataclass(frozen=True)
class Button:
    """What a button cannot be pressed without, and what it may take besides."""

    needs: tuple[str, ...] = ()
    takes: tuple[str, ...] = ()


# A setpoint of None switches the vessel off, and a recirculation takes no
# litres: the controller says the rest, when the executor presses the button
BUTTONS: dict[Command, Button] = {
    Command.ACTIVATE_ROUTE: Button(needs=("route",), takes=("liters",)),
    Command.STOP_ROUTE: Button(),
    Command.SET_TEMPERATURE: Button(needs=("vessel",), takes=("celsius",)),
    Command.SET_AGITATOR: Button(needs=("on",)),
    Command.START_PROGRAM: Button(),
    Command.CONFIRM_STEP: Button(),
    Command.PAUSE_PROGRAM: Button(),
    Command.RESUME_PROGRAM: Button(),
    Command.ABORT_PROGRAM: Button(),
    Command.STOP_ALL: Button(),
    Command.RESET: Button(),
}

# The highest setpoint of each vessel, on its nameplate: adapters/plant_sim/
# layout.py reads it here. The controller refuses a higher one too.
MAX_SETPOINT_C: dict[Vessel, float] = {
    Vessel.HLT: 85.0,
    Vessel.MASH: 80.0,
    Vessel.BOIL: 100.0,
    Vessel.FERM: 30.0,
}
