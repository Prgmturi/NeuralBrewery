from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from neuralbrewery.core.plant import watcher
from neuralbrewery.core.plant.dependencies import PlantReaderDep
from neuralbrewery.core.plant.protocols import SimulationControl
from neuralbrewery.core.state import StateKey
from neuralbrewery.features.plant.schemas import (
    AdvanceRequest,
    AdvanceResponse,
    FaultRequest,
    PlantResponse,
)

# Set by bootstrap.py only when PLANT_SIMULATION_CONTROL is on: a
# SimulationOnly, which can neither read nor command
SIMULATION_CONTROL = StateKey[SimulationControl]("simulation_control")

plant_router = APIRouter(prefix="/plant", tags=["Plant"])
simulation_router = APIRouter(prefix="/simulation", tags=["Simulation"])


def get_simulation_control(request: Request) -> SimulationControl:
    return SIMULATION_CONTROL.get(request.app.state)


SimulationControlDep = Annotated[SimulationControl, Depends(get_simulation_control)]


@plant_router.get("", summary="What the controller shows")
async def read_plant(reader: PlantReaderDep) -> PlantResponse:
    """Readings, devices, regulation, transfer, program and alarms, now."""
    return PlantResponse.model_validate((await reader.snapshot()).model_dump())


@simulation_router.post("/advance", summary="Move the simulated time on")
async def advance(
    payload: AdvanceRequest, control: SimulationControlDep, reader: PlantReaderDep
) -> AdvanceResponse:
    """Move on, then ask the watcher. 422 for a part of a step.

    The plant computes in this process: an hour of brew day blocks the API
    for about 0.16 s.
    """
    await control.advance(payload.seconds)
    state = await reader.snapshot()
    return AdvanceResponse(
        sim_time_s=state.sim_time_s,
        alarms=list(state.alarms),
        judgements=await watcher.check(reader),
    )


@simulation_router.post(
    "/faults", status_code=status.HTTP_204_NO_CONTENT, summary="Inject a fault"
)
async def inject_fault(payload: FaultRequest, control: SimulationControlDep) -> None:
    """422 for a fault its target cannot have (docs/impianto.md, Guasti)."""
    await control.inject_fault(payload)


@simulation_router.delete(
    "/faults", status_code=status.HTTP_204_NO_CONTENT, summary="Clear every fault"
)
async def clear_faults(control: SimulationControlDep) -> None:
    await control.clear_faults()
