"""The ports of the plant: what can be asked of its controller, not how.

Three ports, one for each kind of privilege. The same object may implement
all three: each consumer receives it typed as the one port it may use.

- PlantReader: agents, the MCP server, the watcher.
- PlantCommander: only the executor of approved actions. Never an agent.
- SimulationControl: only tests, evals and the demo. Never in production.

An adapter that cannot reach the plant raises ServiceUnavailableError, and
ExternalServiceError when the answer cannot be used (ADR 0006). A command
the plant refuses is not an error: it is a CommandResult with the reason.
"""

from typing import Protocol, runtime_checkable

from neuralbrewery.core.plant.schemas import (
    CommandResult,
    Event,
    Fault,
    HistorySample,
    PlantState,
    Route,
    Vessel,
)


@runtime_checkable
class PlantReader(Protocol):
    """Reads what the controller knows."""

    async def snapshot(self) -> PlantState: ...

    async def events(self, since_s: float = 0.0) -> list[Event]:
        """The events from that simulated time on, oldest first."""
        ...

    async def history(self, tag: str, since_s: float = 0.0) -> list[HistorySample]:
        """The short history of a reading or of a command, oldest first.

        Raises NotFoundError for a tag the controller does not record.
        """
        ...


@runtime_checkable
class PlantCommander(Protocol):
    """The buttons on the panel of the controller. Every command has an end."""

    async def activate_route(
        self, route: Route, liters: float | None = None
    ) -> CommandResult:
        """Move that many litres, then stop. A recirculation takes no litres."""
        ...

    async def stop_route(self) -> CommandResult: ...

    async def set_temperature(
        self, vessel: Vessel, celsius: float | None
    ) -> CommandResult:
        """Hold the vessel at that temperature; None switches it off."""
        ...

    async def set_agitator(self, on: bool) -> CommandResult: ...

    async def stop_all(self) -> CommandResult:
        """Stop the hot side. The fermenter is left as it is."""
        ...

    async def reset(self) -> CommandResult:
        """Re-arm: whatever the controller or the safety chain stopped may go on."""
        ...


@runtime_checkable
class SimulationControl(Protocol):
    """The hand of whoever runs a test: time and faults."""

    async def advance(self, seconds: float) -> None:
        """Move the simulated time on.

        Raises ValidationError when seconds is not a whole number of
        calculation steps.
        """
        ...

    async def inject_fault(self, fault: Fault) -> None:
        """Raises ValidationError for a fault its target cannot have."""
        ...

    async def clear_faults(self) -> None: ...
