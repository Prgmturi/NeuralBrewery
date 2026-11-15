"""Tests for the persistence of the approvals: the rows and the SQL of the log.

Module under test: src/neuralbrewery/features/approvals/persistence/
Layer: Adapter of the domain's port (fake sessions, SQL compiled for Postgres)

WHY these tests exist: each event commits in a transaction of its own, so
the approval is in the table before the button is pressed; a refusal of
the table must reach the domain as a conflict, not as a 500. These tests
read what the log does; tests/integration/test_approvals.py runs it on a
real Postgres, trigger and constraints included.
"""

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

import pytest
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import IntegrityError

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import ConflictError
from neuralbrewery.features.approvals.domain.proposal import (
    EventKind,
    ProposalEvent,
)
from neuralbrewery.features.approvals.domain.protocols import ProposalLog
from neuralbrewery.features.approvals.persistence.models import ApprovalEventRow
from neuralbrewery.features.approvals.persistence.repository import (
    SqlProposalLog,
    to_event,
)

NOW = datetime(2026, 11, 15, 9, 0, tzinfo=UTC)


def event(proposal_id: UUID, seq: int, kind: EventKind) -> ProposalEvent:
    return ProposalEvent(
        id=uuid4(),
        proposal_id=proposal_id,
        seq=seq,
        kind=kind,
        actor=Actor.MCP,
        by="claude-code",
        data={"command": "reset", "arguments": {}, "why": ""},
        sim_time_s=60.0,
        at=NOW,
    )


def row_of(e: ProposalEvent) -> ApprovalEventRow:
    return ApprovalEventRow(
        id=e.id,
        proposal_id=e.proposal_id,
        seq=e.seq,
        kind=e.kind.value,
        actor=e.actor.value,
        actor_name=e.by,
        data=dict(e.data),
        sim_time_s=e.sim_time_s,
        created_at=e.at,
    )


class FakeSession:
    def __init__(self, results: list[list[Any]]) -> None:
        self.added: list[Any] = []
        self.statements: list[Any] = []
        self._results = results

    def add(self, row: Any) -> None:
        self.added.append(row)

    async def scalars(self, statement: Any) -> Any:
        self.statements.append(statement)
        return iter(self._results.pop(0))


class FakeSessions:
    """async_sessionmaker: sessions() reads, sessions.begin() writes and commits."""

    def __init__(self, *results: list[Any], commit_error: Exception | None = None):
        self.session = FakeSession(list(results))
        self.commits = 0
        self._commit_error = commit_error

    @asynccontextmanager
    async def __call__(self):
        yield self.session

    @asynccontextmanager
    async def begin(self):
        yield self.session
        if self._commit_error is not None:
            raise self._commit_error
        self.commits += 1


def sql(statement: Any) -> str:
    return str(statement.compile(dialect=postgresql.dialect()))


class TestAppend:
    async def test_writes_every_field_and_commits_alone(self):
        """[HP] One row, in a transaction of its own, committed before it returns."""
        sessions = FakeSessions()
        proposed = event(uuid4(), 0, EventKind.PROPOSED)

        await SqlProposalLog(sessions).append(proposed)

        [row] = sessions.session.added
        assert to_event(row) == proposed
        assert sessions.commits == 1

    async def test_a_refusal_of_the_table_is_a_conflict(self):
        """[EC] Another request decided first: 409, not 500."""
        sessions = FakeSessions(commit_error=IntegrityError("INSERT", {}, Exception()))

        with pytest.raises(ConflictError):
            await SqlProposalLog(sessions).append(event(uuid4(), 1, EventKind.APPROVED))


class TestRead:
    async def test_history_is_the_proposal_in_order(self):
        """[HP] Only that proposal's events, by seq; enums come back as enums."""
        proposal_id = uuid4()
        rows = [
            row_of(event(proposal_id, 0, EventKind.PROPOSED)),
            row_of(event(proposal_id, 1, EventKind.REJECTED)),
        ]
        sessions = FakeSessions(rows)

        history = await SqlProposalLog(sessions).history(proposal_id)

        assert [e.kind for e in history] == [EventKind.PROPOSED, EventKind.REJECTED]
        assert history[0].actor is Actor.MCP
        text = sql(sessions.session.statements[0])
        assert "WHERE approval_events.proposal_id = " in text
        assert "ORDER BY approval_events.seq" in text

    async def test_page_is_the_newest_births_with_their_events(self):
        """[HP] Births newest first, one page; each proposal with its events."""
        newer, older = uuid4(), uuid4()
        events = [
            row_of(event(older, 0, EventKind.PROPOSED)),
            row_of(event(newer, 0, EventKind.PROPOSED)),
            row_of(event(older, 1, EventKind.APPROVED)),
        ]
        sessions = FakeSessions([newer, older], events)

        page = await SqlProposalLog(sessions).page(limit=2, offset=4)

        assert [p.id for p in page] == [newer, older]
        assert [e.kind for e in page[1].events] == [
            EventKind.PROPOSED,
            EventKind.APPROVED,
        ]
        births = sql(sessions.session.statements[0])
        assert "WHERE approval_events.seq = " in births
        assert (
            "ORDER BY approval_events.created_at DESC, approval_events.proposal_id DESC"
            in births
        )
        assert "LIMIT" in births and "OFFSET" in births
        assert "approval_events.actor" not in births

    async def test_a_page_of_one_proposer_filters_before_the_limit(self):
        """[SEC] Only the agent's births are counted: MCP proposals push none out."""
        sessions = FakeSessions([], [])

        await SqlProposalLog(sessions).page(limit=10, offset=0, actor=Actor.AGENT)

        statement = sessions.session.statements[0]
        births = sql(statement)
        assert "WHERE approval_events.seq = " in births
        assert "AND approval_events.actor = " in births
        assert births.index("approval_events.actor") < births.index("LIMIT")
        assert "agent" in statement.compile().params.values()


def test_the_log_matches_the_port():
    """[HP] mypy checks it where the api wires it; this checks it at run time."""
    assert isinstance(SqlProposalLog(FakeSessions()), ProposalLog)


def test_the_table_ties_each_kind_to_its_step():
    """[SEC] The check of the table: a decision only at seq 1, an outcome at 2."""
    [check] = [
        c
        for c in ApprovalEventRow.__table__.constraints
        if isinstance(c, CheckConstraint)
    ]

    assert str(check.sqltext) == (
        "(seq = 0 AND kind IN ('blocked', 'proposed')) "
        "OR (seq = 1 AND kind IN ('approved', 'rejected')) "
        "OR (seq = 2 AND kind IN ('executed', 'execution_failed'))"
    )
