"""The alarms active now, and the log of what happened."""

from collections import deque
from collections.abc import Mapping

from neuralbrewery.core.plant.schemas import Alarm, AlarmCode, Event, EventKind

AlarmKey = tuple[AlarmCode, str]  # the code, and the tag it is about

EVENTS_KEPT = 10_000  # the oldest are dropped: an alarm that flaps fills no memory


class Journal:
    def __init__(self) -> None:
        self._active: dict[AlarmKey, Alarm] = {}
        self._events: deque[Event] = deque(maxlen=EVENTS_KEPT)
        self._seq = 0

    @property
    def alarms(self) -> tuple[Alarm, ...]:
        """The active alarms, oldest first."""
        return tuple(self._active.values())

    def events(self, since_s: float) -> list[Event]:
        return [event for event in self._events if event.sim_time_s >= since_s]

    def record(
        self, now_s: float, kind: EventKind, code: str, tag: str, text: str
    ) -> None:
        self._seq += 1
        self._events.append(
            Event(
                seq=self._seq,
                sim_time_s=now_s,
                kind=kind,
                code=code,
                tag=tag,
                text=text,
            )
        )

    def update(self, now_s: float, present: Mapping[AlarmKey, str]) -> None:
        """Take the alarms that hold now: log those that begin and those that end.

        An alarm already active keeps the time and the text it began with.
        """
        for key in [key for key in self._active if key not in present]:
            ended = self._active.pop(key)
            self.record(
                now_s, EventKind.ALARM_CLEARED, ended.code, ended.tag, ended.text
            )
        for key, text in present.items():
            if key not in self._active:
                code, tag = key
                self._active[key] = Alarm(code=code, tag=tag, text=text, since_s=now_s)
                self.record(now_s, EventKind.ALARM_RAISED, code, tag, text)
