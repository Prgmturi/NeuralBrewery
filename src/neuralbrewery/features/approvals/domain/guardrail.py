"""The guardrail: what may enter the queue, checked before it does.

A second level after the interlocks of the controller, not the only one:
a button of the panel, the arguments it needs and no other, names the
plant knows, a setpoint between 0 and the highest of the vessel, litres
above 0. The reasons are for the brewer and for the model that proposed,
in Italian.

The arguments come from JSON (the MCP server) or from a validated
proposal (the plant agent): every type is checked, a bool is no number.
"""

import math
from collections.abc import Mapping
from typing import Any

from neuralbrewery.core.plant.panel import (
    BUTTONS,
    MAX_SETPOINT_C,
    Command,
    Route,
    Vessel,
)

ROUTES = {route.value for route in Route}
VESSELS = {vessel.value for vessel in Vessel}


def refusal(command: str, arguments: Mapping[str, Any]) -> str:
    """Why the proposal may not enter the queue; empty if it may."""
    if command not in BUTTONS:
        buttons = ", ".join(BUTTONS)
        return f"{command!r} non è un pulsante del pannello, che ha: {buttons}."
    button = BUTTONS[Command(command)]
    missing = [name for name in button.needs if arguments.get(name) is None]
    if missing:
        return f"{command} vuole {', '.join(missing)}."
    extra = sorted(set(arguments) - set(button.needs) - set(button.takes))
    if extra:
        return f"{command} non prende {', '.join(extra)}."
    # In the order of the button: the vessel is checked before its setpoint
    for name in (*button.needs, *button.takes):
        if name in arguments and (reason := _argument(name, arguments)):
            return reason
    return ""


def _argument(name: str, arguments: Mapping[str, Any]) -> str:
    value = arguments[name]
    match name:
        # A str first: a list or a dict from JSON cannot be looked up in a set
        case "route" if not isinstance(value, str) or value not in ROUTES:
            return f"route {value!r} non è un percorso: sono {_list(ROUTES)}."
        case "vessel" if not isinstance(value, str) or value not in VESSELS:
            return f"vessel {value!r} non è un recipiente: sono {_list(VESSELS)}."
        case "on" if not isinstance(value, bool):
            return f"on vuole true o false, non {value!r}."
        case "celsius" if value is not None:
            highest = MAX_SETPOINT_C[Vessel(arguments["vessel"])]
            if not _number(value) or not 0 <= value <= highest:
                return (
                    f"Il setpoint di {arguments['vessel']} va da 0 a {highest:g} °C: "
                    f"{value!r} è fuori."
                )
        case "liters" if value is not None and (not _number(value) or value <= 0):
            return f"liters vuole un numero di litri sopra 0, non {value!r}."
    return ""


def _number(value: Any) -> bool:
    """A finite int or float, and not a bool."""
    return (
        isinstance(value, int | float)
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _list(names: set[str]) -> str:
    return ", ".join(sorted(names))
