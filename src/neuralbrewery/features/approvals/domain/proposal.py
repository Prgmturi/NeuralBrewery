"""A proposal is the list of its events, and its status is the last one.

The domain decides ids and times; persistence only stores them.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Self
from uuid import UUID

from neuralbrewery.core.approvals.schemas import Actor


class EventKind(StrEnum):
    PROPOSED = "proposed"  # passed the guardrail: waits for the brewer
    BLOCKED = "blocked"  # stopped by the guardrail: never queued
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"  # the controller answered, a refusal included
    EXECUTION_FAILED = "execution_failed"  # no answer from the plant


BIRTHS = frozenset({EventKind.PROPOSED, EventKind.BLOCKED})
DECISIONS = frozenset({EventKind.APPROVED, EventKind.REJECTED})
OUTCOMES = frozenset({EventKind.EXECUTED, EventKind.EXECUTION_FAILED})
# The seq of an event is its step: 0 the birth, 1 the decision, 2 the
# outcome. One event per step, so one decision and one outcome at most: the
# table enforces it too, with a unique (proposal_id, seq).
STEPS = (BIRTHS, DECISIONS, OUTCOMES)

# The longest name of who acts: the requests and the table take it too
BY_MAX_LENGTH = 100


@dataclass(frozen=True)
class Action:
    """A button of the panel and its arguments, as proposed."""

    command: str
    arguments: Mapping[str, Any]


@dataclass(frozen=True)
class Answer:
    """What the controller said to the button: accepted, or why not."""

    accepted: bool
    code: str
    reason: str


@dataclass(frozen=True)
class ProposalEvent:
    """One step of a proposal. Written once, never changed."""

    id: UUID
    proposal_id: UUID
    seq: int  # 0 for the birth, then one more for each step
    kind: EventKind
    actor: Actor
    by: str  # the name, as declared: nobody checks it
    data: Mapping[str, Any]  # JSON: the action, a reason, the answer
    sim_time_s: float
    at: datetime  # the real time, for the audit only


@dataclass(frozen=True)
class QueuedProposal:
    """A proposal and every event it had, oldest first. Never empty."""

    events: tuple[ProposalEvent, ...]

    @property
    def id(self) -> UUID:
        return self.events[0].proposal_id

    @property
    def status(self) -> EventKind:
        return self.events[-1].kind

    @property
    def action(self) -> Action:
        birth = self.events[0].data
        return Action(birth["command"], birth["arguments"])

    @property
    def why(self) -> str:
        why: str = self.events[0].data.get("why", "")
        return why

    @property
    def blocked_reason(self) -> str:
        """Why the guardrail stopped it; empty if it did not."""
        reason: str = self.events[0].data.get("reason", "")
        return reason

    def then(self, event: ProposalEvent) -> Self:
        return type(self)((*self.events, event))
