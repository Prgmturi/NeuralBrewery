"""One port of the plant and nothing more, whatever object is behind it.

The in-process adapter implements the three ports in one object: handed to
an agent typed as PlantReader, it can still be commanded at run time, and
mypy is the only check. Until the plant-sim service puts a token between
the agents and the commands (milestone M2), these wrappers are the wall:
ReadOnlyPlant has the three reading methods and no other, SimulationOnly
the three of the hand of a test.
"""

from neuralbrewery.core.plant.protocols import PlantReader, SimulationControl
from neuralbrewery.core.plant.schemas import Event, Fault, HistorySample, PlantState


class ReadOnlyPlant:
    def __init__(self, reader: PlantReader) -> None:
        self._reader = reader

    async def snapshot(self) -> PlantState:
        return await self._reader.snapshot()

    async def events(self, since_s: float = 0.0) -> list[Event]:
        return await self._reader.events(since_s)

    async def history(self, tag: str, since_s: float = 0.0) -> list[HistorySample]:
        return await self._reader.history(tag, since_s)


class SimulationOnly:
    def __init__(self, control: SimulationControl) -> None:
        self._control = control

    async def advance(self, seconds: float) -> None:
        await self._control.advance(seconds)

    async def inject_fault(self, fault: Fault) -> None:
        await self._control.inject_fault(fault)

    async def clear_faults(self) -> None:
        await self._control.clear_faults()
