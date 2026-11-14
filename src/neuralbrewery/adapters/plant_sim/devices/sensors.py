"""Measuring instruments: from the true value to the signal the controller gets.

Each instrument has its own random sequence, made from the seed and its
tag: a fault on one does not change the noise of the others, so a scenario
with a fault can be compared with the same scenario without.
"""

import random
from collections.abc import Callable

from neuralbrewery.adapters.plant_sim.layout import HYDROMETER
from neuralbrewery.adapters.plant_sim.signals import HydrometerMessage

# NAMUR NE43, as the iTEMP TMT80 does it (TI00153R, page 2): a healthy
# transmitter stays between the first two, and says "I am faulty" with the third
SATURATION_MA = (3.8, 20.5)
SENSOR_BREAK_MA = 21.5
NO_SIGNAL_MA = 0.0

# Foam on the surface, as section 11.4 of the SICK manual describes it. How
# often and how high are our choice: docs/impianto.md, "Da verificare".
FOAM_JUMP_CHANCE = 0.05  # for each measure
FOAM_JUMP_L = (1.0, 5.0)


def class_a_tolerance_c(temp_c: float) -> float:
    """PT100 class A, IEC 60751 (iTHERM TM411, page 16)."""
    return 0.15 + 0.002 * abs(temp_c)


def level_tolerance_l(_level_l: float) -> float:
    """SICK LFP Cubic: 5 mm (data sheet, page 2), about half a litre here."""
    return 0.5


class Transmitter:
    """A sensor with its 4-20 mA transmitter: a PT100 or a level probe."""

    def __init__(
        self,
        tag: str,
        span: tuple[float, float],
        tolerance: Callable[[float], float],
        noise_sd: float,
        seed: int,
    ) -> None:
        self._low, self._high = span  # the values at 4 mA and at 20 mA
        self._tolerance = tolerance
        self._noise_sd = noise_sd
        self._noise = random.Random(f"{seed}/{tag}")
        self._foam_jumps = random.Random(f"{seed}/{tag}/foam")
        # Where in its tolerance this very instrument sits: fixed for good
        self._bias = self._noise.uniform(-1.0, 1.0)
        self._last_ma = SATURATION_MA[0]
        self.clear_faults()

    def clear_faults(self) -> None:
        self.offset = 0.0
        self.sensor_broken = False
        self.cable_broken = False
        self.foam = False
        self._stuck_ma: float | None = None

    def stick(self, value: float | None) -> None:
        """Freeze the output at that value, or where it is now."""
        self._stuck_ma = self._last_ma if value is None else self._to_ma(value)

    def current_ma(self, true_value: float) -> float:
        """One measure, as the current on the wire."""
        # Drawn at every measure, faulty or not: the sequence stays the same
        noise = self._noise.gauss(0.0, self._noise_sd)
        value = true_value + self._bias * self._tolerance(true_value) + noise
        value += self.offset
        if self.foam and self._foam_jumps.random() < FOAM_JUMP_CHANCE:
            value += self._foam_jumps.uniform(*FOAM_JUMP_L)

        current = self._to_ma(value)
        if self._stuck_ma is not None:
            current = self._stuck_ma
        if self.sensor_broken:
            current = SENSOR_BREAK_MA
        if self.cable_broken:
            current = NO_SIGNAL_MA
        self._last_ma = current
        return current

    def _to_ma(self, value: float) -> float:
        current = 4.0 + 16.0 * (value - self._low) / (self._high - self._low)
        low, high = SATURATION_MA
        return min(max(current, low), high)


# iSpindel: one message every 15 minutes. Battery figures are our choice:
# its README gives none (docs/impianto.md, "Da verificare").
HYDROMETER_PERIOD_S = 900.0
BATTERY_FRESH_V = 4.1
BATTERY_CUTOFF_V = 3.3
BATTERY_DRAIN_V = 0.000125  # for each message: about two months of life
BATTERY_FAILING_DRAIN_V = 0.025  # for each message: about eight hours
WIFI_RSSI_DBM = -60.0


class Hydrometer:
    """The wireless hydrometer floating in the fermenter."""

    def __init__(self, seed: int, on: bool) -> None:
        self._noise = random.Random(f"{seed}/{HYDROMETER}")
        self._gravity_bias = self._noise.uniform(-0.001, 0.001)
        self._temp_bias_c = self._noise.uniform(-0.5, 0.5)
        self._next_at_s = 0.0
        self.on = on  # it is switched on when it goes into the wort
        self.clear_faults()

    def clear_faults(self) -> None:
        """Back to health; a battery that was failing is a new one."""
        self.battery_v = BATTERY_FRESH_V
        self.battery_failing = False
        self.wifi_lost = False

    def message(
        self, now_s: float, gravity: float, temp_c: float
    ) -> HydrometerMessage | None:
        """The message sent at this instant, if one is due and gets through."""
        if not self.on or now_s < self._next_at_s:
            return None
        self._next_at_s = now_s + HYDROMETER_PERIOD_S
        self.battery_v -= (
            BATTERY_FAILING_DRAIN_V if self.battery_failing else BATTERY_DRAIN_V
        )
        if self.wifi_lost or self.battery_v < BATTERY_CUTOFF_V:
            return None
        return HydrometerMessage(
            sent_at_s=now_s,
            gravity=round(
                gravity + self._gravity_bias + self._noise.gauss(0.0, 0.0003), 4
            ),
            temperature_c=round(
                temp_c + self._temp_bias_c + self._noise.gauss(0.0, 0.05), 2
            ),
            battery_v=round(self.battery_v, 2),
            rssi_dbm=round(WIFI_RSSI_DBM + self._noise.gauss(0.0, 2.0)),
        )
