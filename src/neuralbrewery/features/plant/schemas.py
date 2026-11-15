"""What the routes of the plant take and return."""

from pydantic import BaseModel, Field

from neuralbrewery.core.plant.schemas import Alarm, Fault, PlantState, WatcherAlarm

# A day of brew at 1 s steps takes about 4 s of CPU, with the API blocked
MAX_ADVANCE_S = 24 * 3600


class PlantResponse(PlantState):
    """What the controller knows now. Not what is true."""


class AdvanceRequest(BaseModel):
    seconds: float = Field(
        gt=0,
        le=MAX_ADVANCE_S,
        description="Simulated seconds to move on: a whole number of steps",
    )


class AdvanceResponse(BaseModel):
    """Where the plant is after the advance, and what is wrong with it."""

    sim_time_s: float
    alarms: list[Alarm]  # of the controller
    judgements: list[WatcherAlarm]  # of the watcher, which runs after each advance


class FaultRequest(Fault):
    """A fault to inject: kind, target tag, and a value for some kinds."""
