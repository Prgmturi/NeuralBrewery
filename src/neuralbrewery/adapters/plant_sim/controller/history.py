"""The short history: enough for a diagnosis and for the evals, with no database.

A reading is kept as it was at the sample. A command is kept as its mean
since the sample before: a heater that was on for 24 seconds of a minute
is "40 %". The value of the instant would miss most of what an on/off
regulation does.
"""

from collections import deque
from collections.abc import Mapping

from neuralbrewery.core.exceptions import NotFoundError
from neuralbrewery.core.plant.schemas import HistorySample


class History:
    def __init__(self, window_s: int, period_s: int) -> None:
        self._period_s = period_s
        self._kept = window_s // period_s
        self._samples: dict[str, deque[HistorySample]] = {}
        self._command_sums: dict[str, float] = {}
        self._scans = 0
        self._next_at_s = 0.0

    def record(
        self,
        now_s: float,
        readings: Mapping[str, float | None],
        commands: Mapping[str, float],
    ) -> None:
        """Take one scan in; once a period has passed, keep a sample for each tag."""
        for tag, value in commands.items():
            self._command_sums[tag] = self._command_sums.get(tag, 0.0) + value
        self._scans += 1
        if now_s < self._next_at_s:
            return
        self._next_at_s = now_s + self._period_s

        for tag, reading in readings.items():
            self._keep(tag, now_s, reading)
        for tag, total in self._command_sums.items():
            self._keep(tag, now_s, round(total / self._scans, 1))
        self._command_sums.clear()
        self._scans = 0

    def _keep(self, tag: str, now_s: float, value: float | None) -> None:
        samples = self._samples.setdefault(tag, deque(maxlen=self._kept))
        samples.append(HistorySample(sim_time_s=now_s, value=value))

    def since(self, tag: str, since_s: float) -> list[HistorySample]:
        if tag not in self._samples:
            raise NotFoundError("History of tag", tag)
        return [sample for sample in self._samples[tag] if sample.sim_time_s >= since_s]
