"""The wired safety: one thermostat for each heated vessel, in series, and K1.

Wires, not program. It is the only thing in the plant that acts on a true
temperature, and it works whatever the controller believes: a controller
fooled by a faulty level is stopped here. The controller sees one contact
of K1, and cannot tell which thermostat opened it.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.layout import VESSELS
from neuralbrewery.core.plant.schemas import Vessel


@dataclass
class SafetyChain:
    closed: bool = True  # K1: open, no heater has power

    def check(self, temps_c: Mapping[Vessel, float], reset: bool) -> None:
        """Open K1 above a limit; close it on a reset, once all are below."""
        if any(
            temps_c[vessel] > plate.thermostat_c for vessel, plate in VESSELS.items()
        ):
            self.closed = False
        elif reset:
            self.closed = True
