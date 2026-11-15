"""The audit of the approvals on a real Postgres: trigger, constraints, races.

Module under test: src/neuralbrewery/features/approvals/ and its migration
Layer: Persistence and domain, real database (the schema of the migrations)

WHY: the unit tests prove the rules on a log in memory. Here the table
itself refuses what must never happen: a row changed or deleted, by the
owner of the table too, and a second decision, even when two approvals
arrive together and both read "proposed".

No cleanup between tests: the trigger forbids it. Every test makes its own
proposals, with new ids.
"""

import asyncio
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import ConflictError
from neuralbrewery.features.approvals.domain.proposal import EventKind
from neuralbrewery.features.approvals.domain.service import ApprovalQueue
from neuralbrewery.features.approvals.persistence.repository import SqlProposalLog
from tests.features.approvals.fakes import FakePanel, FixedClock


@pytest.fixture
def log(migrated_database, db_manager) -> SqlProposalLog:
    return SqlProposalLog(db_manager.session_factory)


@pytest.fixture
def queue(log) -> ApprovalQueue:
    return ApprovalQueue(log, FixedClock(120.0))


async def proposed(queue: ApprovalQueue):
    return await queue.propose(
        "set_temperature",
        {"vessel": "FERM", "celsius": 18.5},
        Actor.MCP,
        "claude-code",
        "TT5a legge due gradi in più",
    )


class TestStored:
    async def test_the_whole_story_comes_back_the_same(self, queue, log):
        """[HP] proposed, approved, executed: JSONB, times and names round trip."""
        proposal = await proposed(queue)
        done = await queue.approve(proposal.id, "Salvatore", FakePanel())

        stored = await log.history(proposal.id)

        assert stored == list(done.events)
        assert stored[0].data["arguments"] == {"vessel": "FERM", "celsius": 18.5}
        assert stored[0].at.utcoffset().total_seconds() == 0

    async def test_page_shows_the_newest_first(self, queue, log):
        """[HP] The last two proposals, the newest at the top."""
        first = await proposed(queue)
        second = await proposed(queue)

        page = await log.page(limit=2, offset=0)

        assert [p.id for p in page] == [second.id, first.id]


class TestAppendOnly:
    """The trigger of the migration: rows are only added."""

    @pytest.mark.parametrize(
        "statement",
        [
            "UPDATE approval_events SET actor_name = 'qualcun altro' "
            "WHERE proposal_id = :id",
            "DELETE FROM approval_events WHERE proposal_id = :id",
        ],
        ids=["update", "delete"],
    )
    async def test_a_row_cannot_change(self, queue, db_manager, log, statement):
        """[SEC] UPDATE and DELETE refused, for the owner of the table too."""
        proposal = await proposed(queue)

        with pytest.raises(DBAPIError, match="only added"):
            async with db_manager.engine.begin() as connection:
                await connection.execute(text(statement), {"id": proposal.id})

        assert await log.history(proposal.id) == list(proposal.events)

    async def test_the_table_cannot_be_emptied(self, queue, db_manager):
        """[SEC] TRUNCATE refused."""
        await proposed(queue)

        with pytest.raises(DBAPIError, match="only added"):
            async with db_manager.engine.begin() as connection:
                await connection.execute(text("TRUNCATE approval_events"))


class TestOneDecision:
    async def test_two_approvals_at_once_press_once(self, log):
        """[SEC] Both read "proposed"; the unique (proposal_id, seq) stops one.

        WHY: the check on the status happens before either writes. Only the
        table can tell them apart, and it must, before the button.
        """
        clock = FixedClock(120.0)
        proposal = await proposed(ApprovalQueue(log, clock))
        panel = FakePanel()

        results = await asyncio.gather(
            ApprovalQueue(log, clock).approve(proposal.id, "Anna", panel),
            ApprovalQueue(log, clock).approve(proposal.id, "Bruno", panel),
            return_exceptions=True,
        )

        assert len(panel.pressed) == 1
        assert sum(isinstance(r, ConflictError) for r in results) == 1
        kinds = [e.kind for e in await log.history(proposal.id)]
        assert kinds == [EventKind.PROPOSED, EventKind.APPROVED, EventKind.EXECUTED]

    async def test_the_table_refuses_a_second_decision(self, queue, log):
        """[SEC] Approved at seq 1, then rejected at seq 1: the table says no.

        WHY: the race above passes whether the check on the status or the
        table stops the second approval. This one leaves the table alone.
        """
        proposal = await proposed(queue)
        birth = proposal.events[0]

        def decision(kind: EventKind):
            return type(birth)(**{**vars(birth), "id": uuid4(), "seq": 1, "kind": kind})

        await log.append(decision(EventKind.APPROVED))
        with pytest.raises(ConflictError):
            await log.append(decision(EventKind.REJECTED))

        kinds = [e.kind for e in await log.history(proposal.id)]
        assert kinds == [EventKind.PROPOSED, EventKind.APPROVED]

    async def test_a_kind_out_of_its_step_is_refused(self, queue, log):
        """[SEC] An outcome where the decision goes: the check of the table."""
        proposal = await proposed(queue)
        birth = proposal.events[0]
        wrong = type(birth)(
            **{
                **vars(birth),
                "id": uuid4(),
                "seq": 1,
                "kind": EventKind.EXECUTED,
            }
        )

        with pytest.raises(ConflictError):
            await log.append(wrong)
