"""The process: liquids, temperatures, fermentation. The true values.

Nothing here knows how the plant is measured or driven. Each step it is
told the power each vessel receives and where liquid flows, and it moves
on by that much time. Only tests and evals read it, to give the mark: the
app sees what the controller sees.

The model is in docs/impianto.md, "Processo". One litre of water or wort
weighs one kilogram here.
"""

import math
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.layout import VESSELS
from neuralbrewery.core.plant.schemas import Vessel

WATER_J_PER_KG_C = 4186.0
GRAIN_J_PER_KG_C = 1700.0
# The steel of a vessel: little next to its content, and what an empty one
# heats up with. It is why an element left dry overheats in seconds.
STEEL_J_PER_C = 1000.0
GRAIN_RETAINS_L_PER_KG = 1.0  # water that never drains out of the grain
GRAIN_VOLUME_L_PER_KG = 0.67  # room the grain takes in the tun
BOILING_C = 100.0
EVAPORATION_J_PER_KG = 2_257_000.0
EXCHANGER_OUTLET_C = 20.0  # the plate exchanger on the way to the fermenter

# Heat lost to the room. Starting values, to be tuned (docs/impianto.md)
LOSS_W_PER_C: dict[Vessel, float] = {
    Vessel.HLT: 6.0,
    Vessel.MASH: 5.0,
    Vessel.BOIL: 6.0,
    Vessel.FERM: 2.0,
}

# The yeast: an S curve of about five days at 19 °C, faster when warm
FERMENTATION_RATE_PER_S = 2.13e-5
FERMENTATION_REFERENCE_C = 19.0
FERMENTATION_DOUBLES_EVERY_C = 10.0
FERMENTATION_START = 0.01  # where the curve begins when the yeast is pitched
YEAST_HEAT_J_PER_L = 50_000.0  # over a whole fermentation


@dataclass
class TrueVessel:
    capacity_l: float
    loss_w_per_c: float
    temp_c: float
    liquid_l: float = 0.0
    grain_kg: float = 0.0

    @property
    def filled_l(self) -> float:
        """Liquid and grain together: where the surface is."""
        return self.liquid_l + self.grain_kg * GRAIN_VOLUME_L_PER_KG

    @property
    def drainable_l(self) -> float:
        """What a pump can take out: the grain keeps its share."""
        return max(0.0, self.liquid_l - self.grain_kg * GRAIN_RETAINS_L_PER_KG)

    @property
    def heat_capacity_j_per_c(self) -> float:
        return (
            STEEL_J_PER_C
            + self.liquid_l * WATER_J_PER_KG_C
            + self.grain_kg * GRAIN_J_PER_KG_C
        )


@dataclass
class Fermentation:
    original_gravity: float = 1.050
    final_gravity: float = 1.010
    # How far along the S curve, from FERMENTATION_START to 1. None until
    # the yeast is pitched: wort alone does not ferment.
    activity: float | None = None
    stuck: bool = False  # fault: the yeast has stopped

    def pitch(self, progress: float = 0.0) -> None:
        """Add the yeast; progress says how much of the way is already done."""
        self.activity = FERMENTATION_START + progress * (1.0 - FERMENTATION_START)

    @property
    def gravity(self) -> float:
        if self.activity is None:
            return self.original_gravity
        done = (self.activity - FERMENTATION_START) / (1.0 - FERMENTATION_START)
        return self.original_gravity - done * (
            self.original_gravity - self.final_gravity
        )

    def step(self, temp_c: float, dt_s: float) -> float:
        """Move on by dt_s; returns the share of the whole way done in it."""
        if self.activity is None or self.stuck:
            return 0.0
        warmth = math.pow(
            2.0, (temp_c - FERMENTATION_REFERENCE_C) / FERMENTATION_DOUBLES_EVERY_C
        )
        gained = (
            FERMENTATION_RATE_PER_S
            * warmth
            * self.activity
            * (1.0 - self.activity)
            * dt_s
        )
        self.activity += gained
        return gained


@dataclass(frozen=True)
class Flow:
    """Liquid a pump is moving, in litres a second."""

    source: Vessel
    destination: Vessel
    l_per_s: float


class Process:
    def __init__(self, room_c: float = 20.0) -> None:
        """An empty plant, everything at the temperature of the room."""
        self.room_c = room_c
        self.vessels: dict[Vessel, TrueVessel] = {
            vessel: TrueVessel(plate.capacity_l, LOSS_W_PER_C[vessel], room_c)
            for vessel, plate in VESSELS.items()
        }
        self.fermentation = Fermentation()
        self.evaporated_l = 0.0
        self.overflowed_l = 0.0

    def step(
        self, dt_s: float, heat_w: Mapping[Vessel, float], flows: Iterable[Flow]
    ) -> None:
        """Move on by dt_s, with that power into each vessel and those flows."""
        for flow in flows:
            self._move(flow, dt_s)

        wort = self.vessels[Vessel.FERM]
        gained = self.fermentation.step(wort.temp_c, dt_s)
        yeast_w = YEAST_HEAT_J_PER_L * wort.liquid_l * gained / dt_s

        for vessel, content in self.vessels.items():
            extra_w = yeast_w if vessel is Vessel.FERM else 0.0
            self._heat(content, heat_w[vessel] + extra_w, dt_s)

    def _move(self, flow: Flow, dt_s: float) -> None:
        source = self.vessels[flow.source]
        destination = self.vessels[flow.destination]
        moved = min(flow.l_per_s * dt_s, source.drainable_l)
        if flow.source is flow.destination or moved <= 0.0:
            return  # a recirculation, or a pump with nothing to take

        # Only the fermenter is reached through the exchanger
        arrives_c = (
            EXCHANGER_OUTLET_C if flow.destination is Vessel.FERM else source.temp_c
        )
        before = destination.heat_capacity_j_per_c
        arriving = moved * WATER_J_PER_KG_C
        destination.temp_c = (before * destination.temp_c + arriving * arrives_c) / (
            before + arriving
        )
        source.liquid_l -= moved
        destination.liquid_l += moved

        spilled = max(0.0, destination.filled_l - destination.capacity_l)
        destination.liquid_l -= spilled
        self.overflowed_l += spilled

    def _heat(self, content: TrueVessel, power_w: float, dt_s: float) -> None:
        lost_w = content.loss_w_per_c * (content.temp_c - self.room_c)
        temp_c = content.temp_c + (power_w - lost_w) * dt_s / (
            content.heat_capacity_j_per_c
        )
        if temp_c > BOILING_C and content.liquid_l > 0.0:
            # Water does not pass 100 °C: the heat left over boils it away.
            # Once it is all gone, the same heat goes into the dry vessel.
            surplus_j = (temp_c - BOILING_C) * content.heat_capacity_j_per_c
            boiled_l = min(surplus_j / EVAPORATION_J_PER_KG, content.liquid_l)
            content.liquid_l -= boiled_l
            self.evaporated_l += boiled_l
            temp_c = BOILING_C + (surplus_j - boiled_l * EVAPORATION_J_PER_KG) / (
                content.heat_capacity_j_per_c
            )
        content.temp_c = temp_c
