from typing import Annotated

from fastapi import Depends, Request

from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.state import StateKey

# Set by bootstrap.py when the app is built: a ReadOnlyPlant, whatever the
# adapter, so that whoever reads it cannot command
PLANT_READER = StateKey[PlantReader]("plant_reader")


def get_plant_reader(request: Request) -> PlantReader:
    return PLANT_READER.get(request.app.state)


PlantReaderDep = Annotated[PlantReader, Depends(get_plant_reader)]
