"""The ports of the approvals in memory: the log, the panel, the clock.

InMemoryProposalLog keeps the rules of the table: an event is never
changed or deleted, a proposal has one birth, one decision and one
outcome, and the data must be JSON that Postgres takes (no NaN).
"""

import asyncio
import json
from uuid import UUID

from neuralbrewery.core.exceptions import ConflictError
from neuralbrewery.features.approvals.domain.proposal import (
    BIRTHS,
    DECISIONS,
    OUTCOMES,
    Action,
    Answer,
    ProposalEvent,
    QueuedProposal,
)


class InMemoryProposalLog:
    def __init__(self) -> None:
        self.events: list[ProposalEvent] = []

    async def append(self, event: ProposalEvent) -> None:
        json.dumps(dict(event.data), allow_nan=False)  # what JSONB refuses
        mine = [e for e in self.events if e.proposal_id == event.proposal_id]
        for step in (BIRTHS, DECISIONS, OUTCOMES):
            if event.kind in step and any(e.kind in step for e in mine):
                raise ConflictError("already decided", resource="Proposal")
        if any(e.seq == event.seq for e in mine):
            raise ConflictError("already decided", resource="Proposal")
        self.events.append(event)

    async def history(self, proposal_id: UUID) -> list[ProposalEvent]:
        # A real query waits for the database: two requests interleave here
        await asyncio.sleep(0)
        mine = [e for e in self.events if e.proposal_id == proposal_id]
        return sorted(mine, key=lambda e: e.seq)

    async def page(self, limit: int, offset: int) -> list[QueuedProposal]:
        births = sorted(
            (e for e in self.events if e.seq == 0),
            key=lambda e: (e.at, e.proposal_id),
            reverse=True,
        )
        return [
            QueuedProposal(tuple(await self.history(birth.proposal_id)))
            for birth in births[offset : offset + limit]
        ]


class FakePanel:
    """The executor's port: records each button pressed, answers as told."""

    def __init__(
        self,
        answer: Answer | None = None,
        *,
        raises: Exception | None = None,
        hangs: bool = False,
    ) -> None:
        self.pressed: list[Action] = []
        self._answer = answer or Answer(accepted=True, code="ok", reason="")
        self._raises = raises
        self._hangs = hangs

    async def press(self, action: Action) -> Answer:
        self.pressed.append(action)
        if self._hangs:
            await asyncio.Event().wait()
        if self._raises is not None:
            raise self._raises
        return self._answer


class FixedClock:
    """Simulated time that moves only when the test says so."""

    def __init__(self, now: float = 0.0) -> None:
        self.time = now

    async def now(self) -> float:
        return self.time
