import asyncio
import math
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import (
    AppExceptionError,
    ConflictError,
    NotFoundError,
)
from neuralbrewery.features.approvals.domain.guardrail import refusal
from neuralbrewery.features.approvals.domain.proposal import (
    EventKind,
    ProposalEvent,
    QueuedProposal,
)
from neuralbrewery.features.approvals.domain.protocols import (
    Panel,
    ProposalLog,
    SimClock,
)

# How long the executor waits for the plant. With the plant in the process
# a command answers at once: the limit matters with the service of M2.
EXECUTION_TIMEOUT_S = 10.0
EXECUTOR = "executor"


class ApprovalQueue:
    """The rules of the queue. Approval is code, never a decision of a model.

    - a proposal enters only through the guardrail; out of limits it is
      blocked, and the block is written;
    - only a proposal waiting for the brewer is approved or rejected;
    - an approved proposal is pressed at once, once, and its outcome is
      written: the controller's answer, or why there was none.

    approve() takes the panel as an argument: whoever builds the queue to
    propose (the MCP server, an agent) has no panel to hand it.
    """

    def __init__(
        self,
        log: ProposalLog,
        clock: SimClock,
        *,
        timeout_s: float = EXECUTION_TIMEOUT_S,
    ) -> None:
        self._log = log
        self._clock = clock
        self._timeout_s = timeout_s

    async def propose(
        self,
        command: str,
        arguments: Mapping[str, Any],
        actor: Actor,
        by: str,
        why: str,
    ) -> QueuedProposal:
        """Queue the proposal, or block it with the reason. Both are written."""
        reason = refusal(command, arguments)
        data = {"command": command, "arguments": dict(arguments), "why": why}
        if reason:
            data["reason"] = reason
        kind = EventKind.BLOCKED if reason else EventKind.PROPOSED
        event = await self._event(uuid4(), 0, kind, actor, by, data)
        await self._log.append(event)
        return QueuedProposal((event,))

    async def get(self, proposal_id: UUID) -> QueuedProposal:
        """Raises NotFoundError if there is no such proposal."""
        events = await self._log.history(proposal_id)
        if not events:
            raise NotFoundError("Proposal", str(proposal_id))
        return QueuedProposal(tuple(events))

    async def page(self, limit: int, offset: int) -> list[QueuedProposal]:
        return await self._log.page(limit, offset)

    async def reject(self, proposal_id: UUID, by: str, reason: str) -> QueuedProposal:
        """Raises NotFoundError, or ConflictError if it is not waiting."""
        proposal = await self._waiting(proposal_id)
        return await self._add(
            proposal, EventKind.REJECTED, Actor.USER, by, {"reason": reason}
        )

    async def approve(self, proposal_id: UUID, by: str, panel: Panel) -> QueuedProposal:
        """Approve, press the button, write the outcome.

        Raises NotFoundError, or ConflictError if the proposal is not
        waiting, a second approval among them. The approval is written
        before the button is pressed: a second request finds it, or the
        log refuses its own.
        """
        proposal = await self._waiting(proposal_id)
        proposal = await self._add(proposal, EventKind.APPROVED, Actor.USER, by, {})
        try:
            async with asyncio.timeout(self._timeout_s):
                answer = await panel.press(proposal.action)
        except TimeoutError:
            error = f"Nessuna risposta dall'impianto entro {self._timeout_s:g} s."
            return await self._failed(proposal, error)
        except AppExceptionError as exc:
            return await self._failed(proposal, exc.message)
        outcome = {
            "accepted": answer.accepted,
            "code": answer.code,
            "reason": answer.reason,
        }
        return await self._add(
            proposal, EventKind.EXECUTED, Actor.EXECUTOR, EXECUTOR, outcome
        )

    async def _waiting(self, proposal_id: UUID) -> QueuedProposal:
        proposal = await self.get(proposal_id)
        if proposal.status is not EventKind.PROPOSED:
            raise ConflictError(
                f"La proposta è {proposal.status}: si decide solo una proposta "
                "in attesa (proposed).",
                resource="Proposal",
            )
        return proposal

    async def _failed(self, proposal: QueuedProposal, error: str) -> QueuedProposal:
        return await self._add(
            proposal,
            EventKind.EXECUTION_FAILED,
            Actor.EXECUTOR,
            EXECUTOR,
            {"error": error},
        )

    async def _add(
        self,
        proposal: QueuedProposal,
        kind: EventKind,
        actor: Actor,
        by: str,
        data: dict[str, Any],
    ) -> QueuedProposal:
        event = await self._event(
            proposal.id, len(proposal.events), kind, actor, by, data
        )
        await self._log.append(event)
        return proposal.then(event)

    async def _event(
        self,
        proposal_id: UUID,
        seq: int,
        kind: EventKind,
        actor: Actor,
        by: str,
        data: dict[str, Any],
    ) -> ProposalEvent:
        return ProposalEvent(
            id=uuid4(),
            proposal_id=proposal_id,
            seq=seq,
            kind=kind,
            actor=actor,
            by=_storable(by),
            data=_storable(data),
            sim_time_s=await self._clock.now(),
            at=datetime.now(UTC),
        )


def _storable[T](value: T) -> T:
    """The value as JSONB takes it: NaN and infinities as text, no NUL byte.

    An MCP client can send both, and a blocked proposal is written as it
    came: Postgres would refuse the whole event.
    """
    stored: Any
    if isinstance(value, float) and not math.isfinite(value):
        stored = str(value)
    elif isinstance(value, str):
        stored = value.replace("\x00", "")
    elif isinstance(value, dict):
        stored = {_storable(key): _storable(item) for key, item in value.items()}
    elif isinstance(value, list):
        stored = [_storable(item) for item in value]
    else:
        stored = value
    result: T = stored
    return result
