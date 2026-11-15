from typing import Protocol, runtime_checkable
from uuid import UUID

from neuralbrewery.features.approvals.domain.proposal import (
    Action,
    Answer,
    ProposalEvent,
    QueuedProposal,
)


@runtime_checkable
class ProposalLog(Protocol):
    """Where the events of the proposals are kept: added, never changed.

    persistence/repository.py implements it on Postgres, each event in a
    transaction of its own: the approval is written before the button is
    pressed.
    """

    async def append(self, event: ProposalEvent) -> None:
        """Add one event.

        Raises ConflictError when the proposal already has an event of that
        step (a second decision, a second outcome) or of that seq: another
        request got there first.
        """
        ...

    async def history(self, proposal_id: UUID) -> list[ProposalEvent]:
        """Every event of the proposal, oldest first; empty if there is none."""
        ...

    async def page(self, limit: int, offset: int) -> list[QueuedProposal]:
        """One page of proposals, the newest first."""
        ...


@runtime_checkable
class Panel(Protocol):
    """The buttons of the plant, for the executor and nobody else."""

    async def press(self, action: Action) -> Answer:
        """Press the button of an approved proposal.

        A refusal of the controller is an Answer, not an error. Raises an
        AppExceptionError when the plant cannot be reached.
        """
        ...


@runtime_checkable
class SimClock(Protocol):
    """The simulated time of the plant, for every event (AGENTS.md, rule 5)."""

    async def now(self) -> float: ...
