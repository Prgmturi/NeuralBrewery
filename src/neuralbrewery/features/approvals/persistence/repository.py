from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import ConflictError
from neuralbrewery.features.approvals.domain.proposal import (
    EventKind,
    ProposalEvent,
    QueuedProposal,
)
from neuralbrewery.features.approvals.persistence.models import ApprovalEventRow


def to_event(row: ApprovalEventRow) -> ProposalEvent:
    """The event of the domain, from its row."""
    return ProposalEvent(
        id=row.id,
        proposal_id=row.proposal_id,
        seq=row.seq,
        kind=EventKind(row.kind),
        actor=Actor(row.actor),
        by=row.actor_name,
        data=row.data,
        sim_time_s=row.sim_time_s,
        at=row.created_at,
    )


class SqlProposalLog:
    """The ProposalLog port on Postgres.

    Not the session of the request: each event is written and committed
    in a transaction of its own, so the approval is in the table before the
    executor presses the button, and a second approval at the same time
    fails on the unique (proposal_id, seq) instead of pressing it again.
    """

    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def append(self, event: ProposalEvent) -> None:
        try:
            async with self._sessions.begin() as session:
                session.add(
                    ApprovalEventRow(
                        id=event.id,
                        proposal_id=event.proposal_id,
                        seq=event.seq,
                        kind=event.kind.value,
                        actor=event.actor.value,
                        actor_name=event.by,
                        data=dict(event.data),
                        sim_time_s=event.sim_time_s,
                        created_at=event.at,
                    )
                )
        except IntegrityError as error:
            raise ConflictError(
                "Un'altra richiesta ha già deciso questa proposta.",
                resource="Proposal",
            ) from error

    async def history(self, proposal_id: UUID) -> list[ProposalEvent]:
        statement = (
            select(ApprovalEventRow)
            .where(ApprovalEventRow.proposal_id == proposal_id)
            .order_by(ApprovalEventRow.seq)
        )
        async with self._sessions() as session:
            return [to_event(row) for row in await session.scalars(statement)]

    async def page(self, limit: int, offset: int) -> list[QueuedProposal]:
        # The births, newest first; two can share created_at: the id keeps
        # the order the same on every page
        births = (
            select(ApprovalEventRow.proposal_id)
            .where(ApprovalEventRow.seq == 0)
            .order_by(
                ApprovalEventRow.created_at.desc(), ApprovalEventRow.proposal_id.desc()
            )
            .limit(limit)
            .offset(offset)
        )
        async with self._sessions() as session:
            ids = list(await session.scalars(births))
            events = select(ApprovalEventRow).where(
                ApprovalEventRow.proposal_id.in_(ids)
            )
            rows = await session.scalars(events.order_by(ApprovalEventRow.seq))
            by_proposal: dict[UUID, list[ProposalEvent]] = {id_: [] for id_ in ids}
            for row in rows:
                by_proposal[row.proposal_id].append(to_event(row))
        return [QueuedProposal(tuple(by_proposal[id_])) for id_ in ids]
