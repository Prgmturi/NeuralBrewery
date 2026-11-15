from neuralbrewery.core.plant.protocols import PlantReader


class PlantClock:
    """The SimClock of the domain: the simulated time the controller shows."""

    def __init__(self, reader: PlantReader) -> None:
        self._reader = reader

    async def now(self) -> float:
        return (await self._reader.snapshot()).sim_time_s
