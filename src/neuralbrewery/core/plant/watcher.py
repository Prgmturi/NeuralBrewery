"""The watcher: fixed rules that judge the process, with no LLM.

The controller reports facts ("TT5b gives no signal"); the watcher judges
what those facts mean together ("the two probes of the fermenter do not
agree"). Its alarms start a diagnosis.

It reads the plant through PlantReader only, and keeps nothing between two
calls: it is called on request, after the time moves on or from a tool of
an agent, never by a loop of its own. With the time in steps the plant is
still between two calls, so the same seed and the same actions give the
same judgements.

The rules are in docs/impianto.md, "Allarmi ed eventi". One for now: a rule
is added when a scenario needs it.
"""

from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.schemas import (
    PlantState,
    Quality,
    Vessel,
    WatcherAlarm,
    WatcherCode,
)

# Two PT100 of class A at 19 °C may be 0.4 °C apart, with the noise a little
# more (docs/impianto.md, check 8). 1 °C is a fault, not a tolerance.
PROBES = ("TT5a", "TT5b")
APART_C = 1.0
# A disagreement must last, so that one sample is never a judgement
LASTING_S = 600


async def check(reader: PlantReader) -> list[WatcherAlarm]:
    """What the watcher judges wrong in the process now; empty if nothing."""
    state = await reader.snapshot()
    found = [await _probes_disagree(reader, state)]
    return [alarm for alarm in found if alarm is not None]


async def _probes_disagree(
    reader: PlantReader, state: PlantState
) -> WatcherAlarm | None:
    """TT5a and TT5b more than APART_C apart, now and for LASTING_S.

    A faulty probe has no value to compare: the controller already reports
    it, with signal_fault.
    """
    now = [state.readings[tag] for tag in PROBES]
    if any(reading.quality is not Quality.GOOD for reading in now):
        return None
    first, second = (reading.value for reading in now)
    if first is None or second is None or abs(first - second) <= APART_C:
        return None

    # Since when: the first sample of the last run of samples that disagree
    first_history = await reader.history(PROBES[0])
    second_history = await reader.history(PROBES[1])
    since_s = state.sim_time_s
    for one, other in zip(
        reversed(first_history), reversed(second_history), strict=True
    ):
        if (
            one.value is None
            or other.value is None
            or abs(one.value - other.value) <= APART_C
        ):
            break
        since_s = one.sim_time_s
    if state.sim_time_s - since_s < LASTING_S:
        return None

    minutes = round((state.sim_time_s - since_s) / 60)
    return WatcherAlarm(
        code=WatcherCode.PROBES_DISAGREE,
        tag=Vessel.FERM,
        text=(
            f"TT5a e TT5b non concordano: {first:.1f} °C contro {second:.1f} °C, "
            f"da {minutes} min"
        ),
        since_s=since_s,
    )
