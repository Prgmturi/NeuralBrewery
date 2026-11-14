"""From a signal to a measure: the value, and how far to trust it.

For a 4-20 mA signal the controller judges the current alone (NAMUR NE43).
It learns that an instrument is faulty, never why: the reason is on the
display of the instrument, for the brewer to read.
"""

from dataclasses import dataclass

from neuralbrewery.adapters.plant_sim.layout import (
    HYDROMETER,
    LEVELS,
    PROBES,
    TEMPERATURE_SPAN_C,
    VESSELS,
)
from neuralbrewery.adapters.plant_sim.signals import HydrometerMessage
from neuralbrewery.core.plant.schemas import Quality

NO_SIGNAL_BELOW_MA = 1.0  # a broken cable, or an instrument with no power
FAULT_AT_MOST_MA = 3.6
FAULT_AT_LEAST_MA = 21.0
HYDROMETER_SILENT_AFTER_S = 1800.0  # two messages missed

# The four numbers in a message of the hydrometer, in the order they come
HYDROMETER_TAGS = (
    HYDROMETER,
    f"{HYDROMETER}.temperature",
    f"{HYDROMETER}.battery",
    f"{HYDROMETER}.rssi",
)

# How each transmitter is ranged: the values at 4 mA and at 20 mA
SPANS: dict[str, tuple[float, float]] = {
    **dict.fromkeys(PROBES, TEMPERATURE_SPAN_C),
    **{tag: (0.0, VESSELS[vessel].capacity_l) for tag, vessel in LEVELS.items()},
}
UNITS: dict[str, str] = {
    **dict.fromkeys(PROBES, "°C"),
    **dict.fromkeys(LEVELS, "L"),
    **dict(zip(HYDROMETER_TAGS, ("SG", "°C", "V", "dBm"), strict=True)),
}


@dataclass(frozen=True, slots=True)
class Measure:
    value: float | None  # None: nothing to trust
    quality: Quality
    reason: str
    current_ma: float | None
    at_s: float


def from_current(current_ma: float, span: tuple[float, float], now_s: float) -> Measure:
    """Read a 4-20 mA signal."""
    shown_ma = round(current_ma, 2)
    if current_ma < NO_SIGNAL_BELOW_MA:
        return Measure(None, Quality.BAD, "segnale assente", shown_ma, now_s)
    if current_ma <= FAULT_AT_MOST_MA or current_ma >= FAULT_AT_LEAST_MA:
        return Measure(None, Quality.BAD, "strumento guasto", shown_ma, now_s)
    low, high = span
    share = (min(max(current_ma, 4.0), 20.0) - 4.0) / 16.0
    value = round(low + share * (high - low), 2)
    return Measure(value, Quality.GOOD, "", shown_ma, now_s)


def from_hydrometer(
    message: HydrometerMessage | None, now_s: float
) -> dict[str, Measure]:
    """The four measures of the last message, stale once it is too old."""
    if message is None:
        never = Measure(None, Quality.STALE, "nessun messaggio ricevuto", None, 0.0)
        return dict.fromkeys(HYDROMETER_TAGS, never)
    if now_s - message.sent_at_s > HYDROMETER_SILENT_AFTER_S:
        quality, reason = Quality.STALE, "nessun messaggio da più di 30 minuti"
    else:
        quality, reason = Quality.GOOD, ""
    values = (
        message.gravity,
        message.temperature_c,
        message.battery_v,
        message.rssi_dbm,
    )
    return {
        tag: Measure(value, quality, reason, None, message.sent_at_s)
        for tag, value in zip(HYDROMETER_TAGS, values, strict=True)
    }
