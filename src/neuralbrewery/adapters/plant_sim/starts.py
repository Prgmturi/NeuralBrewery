"""The named starts: a plant ready for a brew day, or in mid fermentation.

A scenario begins from one of these, never from a plant half way through
both. The step is 1 s on brew day, where a transfer lasts a minute, and
10 s for a fermentation, which lasts days.
"""

from neuralbrewery.adapters.plant_sim.process import Process
from neuralbrewery.adapters.plant_sim.simulator import (
    HISTORY_PERIOD_S,
    HISTORY_WINDOW_S,
    PlantSimulator,
)
from neuralbrewery.core.plant.schemas import Vessel

HLT_WATER_L = 35.0
GRAIN_KG = 4.5
BATCH_L = 20.0
FERMENTATION_C = 19.0


def brew_day(
    *,
    seed: int = 42,
    step_s: int = 1,
    room_c: float = 20.0,
    history_window_s: int = HISTORY_WINDOW_S,
    history_period_s: int = HISTORY_PERIOD_S,
) -> PlantSimulator:
    """Water in the HLT, dry grain in the tun, kettle and fermenter empty.

    The hydrometer is off: it goes into the fermenter with the yeast.
    """
    process = Process(room_c)
    process.vessels[Vessel.HLT].liquid_l = HLT_WATER_L
    process.vessels[Vessel.MASH].grain_kg = GRAIN_KG
    return PlantSimulator(
        process,
        seed=seed,
        step_s=step_s,
        history_window_s=history_window_s,
        history_period_s=history_period_s,
    )


def fermentation(
    *,
    progress: float = 0.0,
    seed: int = 42,
    step_s: int = 10,
    room_c: float = 20.0,
    history_window_s: int = HISTORY_WINDOW_S,
    history_period_s: int = HISTORY_PERIOD_S,
) -> PlantSimulator:
    """Hot side empty and off; 20 L fermenting, held at 19 °C.

    progress is how much of the fermentation is done, from 0 (the yeast
    has just been pitched) to 1.
    """
    process = Process(room_c)
    wort = process.vessels[Vessel.FERM]
    wort.liquid_l, wort.temp_c = BATCH_L, FERMENTATION_C
    process.fermentation.pitch(progress)
    simulator = PlantSimulator(
        process,
        seed=seed,
        step_s=step_s,
        hydrometer_on=True,
        history_window_s=history_window_s,
        history_period_s=history_period_s,
    )
    simulator.controller.set_temperature(Vessel.FERM, FERMENTATION_C)
    return simulator
