"""The in-process adapter: the three ports on a plant in the same process.

For tests and evals: fast, with no service to start, and the same seed
gives the same plant.

One object implements all three ports. Each consumer receives it typed as
the one port it may use, and mypy reports a watcher that calls
activate_route(). That is a check on the code, not a wall at run time: the
wall is the token of the executor, at the border of the plant-sim service
(milestone M2).
"""

from neuralbrewery.adapters.plant_sim.simulator import PlantSimulator
from neuralbrewery.core.plant.schemas import (
    CommandResult,
    Event,
    Fault,
    HistorySample,
    PlantState,
    Route,
    Vessel,
)


class InProcessPlant:
    def __init__(self, simulator: PlantSimulator) -> None:
        self._simulator = simulator
        self._controller = simulator.controller

    # PlantReader

    async def snapshot(self) -> PlantState:
        return self._controller.snapshot()

    async def events(self, since_s: float = 0.0) -> list[Event]:
        return self._controller.events(since_s)

    async def history(self, tag: str, since_s: float = 0.0) -> list[HistorySample]:
        return self._controller.history(tag, since_s)

    # PlantCommander

    async def activate_route(
        self, route: Route, liters: float | None = None
    ) -> CommandResult:
        return self._controller.activate_route(route, liters)

    async def stop_route(self) -> CommandResult:
        return self._controller.stop_route()

    async def set_temperature(
        self, vessel: Vessel, celsius: float | None
    ) -> CommandResult:
        return self._controller.set_temperature(vessel, celsius)

    async def set_agitator(self, on: bool) -> CommandResult:
        return self._controller.set_agitator(on)

    async def start_program(self) -> CommandResult:
        return self._controller.start_program()

    async def confirm_step(self) -> CommandResult:
        # Through the simulator: at the last step the brewer's hands act too
        return self._simulator.confirm_step()

    async def pause_program(self) -> CommandResult:
        return self._controller.pause_program()

    async def resume_program(self) -> CommandResult:
        return self._controller.resume_program()

    async def abort_program(self) -> CommandResult:
        return self._controller.abort_program()

    async def stop_all(self) -> CommandResult:
        return self._controller.stop_all()

    async def reset(self) -> CommandResult:
        return self._controller.reset()

    # SimulationControl

    async def advance(self, seconds: float) -> None:
        self._simulator.advance(seconds)

    async def inject_fault(self, fault: Fault) -> None:
        self._simulator.inject_fault(fault)

    async def clear_faults(self) -> None:
        self._simulator.clear_faults()
