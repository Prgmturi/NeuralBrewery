"""A reader of the plant and nothing more, whatever object is behind it.

The in-process adapter implements the three ports in one object: handed to
an agent typed as PlantReader, it can still be commanded at run time, and
mypy is the only check. Until the plant-sim service puts a token between
the agents and the commands (milestone M2), this wrapper is the wall: what
it holds has the three reading methods, and no other.
"""

from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.schemas import Event, HistorySample, PlantState


class ReadOnlyPlant:
    def __init__(self, reader: PlantReader) -> None:
        self._reader = reader

    async def snapshot(self) -> PlantState:
        return await self._reader.snapshot()

    async def events(self, since_s: float = 0.0) -> list[Event]:
        return await self._reader.events(since_s)

    async def history(self, tag: str, since_s: float = 0.0) -> list[HistorySample]:
        return await self._reader.history(tag, since_s)
