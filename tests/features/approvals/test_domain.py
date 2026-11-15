"""Tests for the rules of the queue of approvals, on ports kept in memory.

Module under test: src/neuralbrewery/features/approvals/domain/
Layer: Business layer, plain Python, no database

WHY these tests exist: an action reaches the plant only after the brewer
approves it (AGENTS.md, rule 1). These are the rules that make it so:
nothing out of limits enters the queue, nothing runs without approval, an
approved proposal runs once, a rejected one never, and every step stays
written.
"""

import asyncio
import math
from uuid import uuid4

import pytest

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import (
    ConflictError,
    NotFoundError,
    ServiceUnavailableError,
)
from neuralbrewery.features.approvals.domain.guardrail import refusal
from neuralbrewery.features.approvals.domain.proposal import (
    Action,
    Answer,
    EventKind,
)
from neuralbrewery.features.approvals.domain.service import ApprovalQueue
from tests.features.approvals.fakes import FakePanel, FixedClock, InMemoryProposalLog

SETPOINT = ("set_temperature", {"vessel": "FERM", "celsius": 18.0})


@pytest.fixture
def log() -> InMemoryProposalLog:
    return InMemoryProposalLog()


@pytest.fixture
def clock() -> FixedClock:
    return FixedClock(3600.0)


@pytest.fixture
def queue(log, clock) -> ApprovalQueue:
    return ApprovalQueue(log, clock, timeout_s=0.05)


async def proposed(queue: ApprovalQueue, command=SETPOINT[0], arguments=None):
    """A proposal of the MCP client that passed the guardrail."""
    proposal = await queue.propose(
        command,
        SETPOINT[1] if arguments is None else arguments,
        Actor.MCP,
        "claude-code",
        "TT5a legge due gradi in più",
    )
    assert proposal.status is EventKind.PROPOSED
    return proposal


class TestGuardrail:
    """Before the queue: a real button, its arguments, and within limits."""

    @pytest.mark.parametrize(
        ("command", "arguments", "says"),
        [
            ("open_valve", {"tag": "EV9"}, "non è un pulsante"),
            ("activate_route", {}, "route"),
            ("set_temperature", {"celsius": 20.0}, "vessel"),
            ("set_agitator", {}, "on"),
            ("stop_all", {"now": True}, "now"),
            ("set_temperature", {"vessel": "FERM", "liters": 3}, "liters"),
            ("activate_route", {"route": "hlt_to_ferm"}, "hlt_to_ferm"),
            ("set_temperature", {"vessel": "KEG", "celsius": 4.0}, "KEG"),
            ("set_temperature", {"vessel": "FERM", "celsius": 31.0}, "30"),
            ("set_temperature", {"vessel": "BOIL", "celsius": 100.5}, "100"),
            ("set_temperature", {"vessel": "HLT", "celsius": -1.0}, "0"),
            ("set_temperature", {"vessel": "HLT", "celsius": math.nan}, "nan"),
            ("set_temperature", {"vessel": "HLT", "celsius": math.inf}, "inf"),
            ("set_temperature", {"vessel": "HLT", "celsius": "70"}, "70"),
            ("set_temperature", {"vessel": "HLT", "celsius": True}, "True"),
            ("activate_route", {"route": "hlt_to_mash", "liters": 0}, "0"),
            ("activate_route", {"route": "hlt_to_mash", "liters": -5.0}, "-5"),
            ("activate_route", {"route": 3, "liters": 5.0}, "3"),
            ("set_agitator", {"on": "true"}, "true"),
            ("set_agitator", {"on": 1}, "1"),
        ],
        ids=[
            "no-such-button",
            "route-missing",
            "vessel-missing",
            "on-missing",
            "argument-of-no-button",
            "argument-of-another-button",
            "no-such-route",
            "no-such-vessel",
            "setpoint-above-the-fermenter",
            "setpoint-above-the-kettle",
            "setpoint-below-zero",
            "setpoint-nan",
            "setpoint-infinite",
            "setpoint-as-text",
            "setpoint-as-bool",
            "no-litres",
            "negative-litres",
            "route-not-a-name",
            "on-as-text",
            "on-as-number",
        ],
    )
    def test_out_of_limits_is_refused_with_the_reason(self, command, arguments, says):
        """[SEC] The reason names what is wrong, for the brewer and the model."""
        assert says in refusal(command, arguments)

    @pytest.mark.parametrize(
        ("command", "arguments"),
        [
            ("reset", {}),
            ("activate_route", {"route": "mash_recirc"}),
            ("activate_route", {"route": "hlt_to_mash", "liters": 12}),
            ("activate_route", {"route": "hlt_to_mash", "liters": None}),
            ("set_temperature", {"vessel": "FERM"}),
            ("set_temperature", {"vessel": "FERM", "celsius": None}),
            ("set_temperature", {"vessel": "FERM", "celsius": 30}),
            ("set_temperature", {"vessel": "MASH", "celsius": 0.0}),
            ("set_agitator", {"on": False}),
        ],
        ids=[
            "no-arguments",
            "recirculation-without-litres",
            "litres-as-int",
            "litres-none",
            "switch-off",
            "switch-off-explicit",
            "setpoint-at-the-limit",
            "setpoint-zero",
            "agitator-off",
        ],
    )
    def test_within_limits_passes(self, command, arguments):
        """[HP] A setpoint at the limit, a switch-off, a stop: they enter."""
        assert refusal(command, arguments) == ""


class TestPropose:
    async def test_enters_the_queue_waiting_for_the_brewer(self, queue, log):
        """[HP] One event, proposed, with who, why and the simulated time."""
        proposal = await proposed(queue)

        [event] = log.events
        assert event.proposal_id == proposal.id
        assert (event.kind, event.actor, event.by) == (
            EventKind.PROPOSED,
            Actor.MCP,
            "claude-code",
        )
        assert event.data == {
            "command": "set_temperature",
            "arguments": {"vessel": "FERM", "celsius": 18.0},
            "why": "TT5a legge due gradi in più",
        }
        assert event.sim_time_s == 3600.0
        assert proposal.action == Action("set_temperature", SETPOINT[1])

    async def test_out_of_limits_is_blocked_and_stays_written(self, queue, log):
        """[SEC] Blocked, not queued; the reason goes back and stays in the audit."""
        proposal = await queue.propose(
            "set_temperature",
            {"vessel": "FERM", "celsius": 45.0},
            Actor.AGENT,
            "plant_agent",
            "",
        )

        assert proposal.status is EventKind.BLOCKED
        assert "30" in proposal.blocked_reason
        [event] = log.events
        assert event.data["reason"] == proposal.blocked_reason
        assert event.data["arguments"] == {"vessel": "FERM", "celsius": 45.0}

    async def test_what_postgres_cannot_store_is_kept_as_text(self, queue, log):
        """[EC] NaN, infinity and a NUL byte from an MCP client: blocked, storable."""
        proposal = await queue.propose(
            "set_temperature",
            {"vessel": "FERM", "celsius": math.nan, "extra": [math.inf]},
            Actor.MCP,
            "a\x00b",
            "why\x00",
        )

        assert proposal.status is EventKind.BLOCKED
        [event] = log.events
        assert event.data["arguments"] == {
            "vessel": "FERM",
            "celsius": "nan",
            "extra": ["inf"],
        }
        assert (event.by, event.data["why"]) == ("ab", "why")


class TestApprove:
    async def test_presses_the_button_once_and_records_the_answer(self, queue, log):
        """[HP] proposed, approved, executed: the action reached the plant once."""
        proposal = await proposed(queue)
        panel = FakePanel(Answer(accepted=True, code="ok", reason=""))

        done = await queue.approve(proposal.id, "Salvatore", panel)

        assert panel.pressed == [Action("set_temperature", SETPOINT[1])]
        assert [e.kind for e in done.events] == [
            EventKind.PROPOSED,
            EventKind.APPROVED,
            EventKind.EXECUTED,
        ]
        approved, executed = done.events[1:]
        assert (approved.actor, approved.by) == (Actor.USER, "Salvatore")
        assert executed.actor is Actor.EXECUTOR
        assert executed.data == {"accepted": True, "code": "ok", "reason": ""}
        assert log.events == list(done.events)

    async def test_a_refusal_of_an_interlock_is_an_answer(self, queue):
        """[HP] Executed, refused by the controller: written, not an error."""
        proposal = await proposed(queue)
        panel = FakePanel(
            Answer(accepted=False, code="level_low", reason="livello basso")
        )

        done = await queue.approve(proposal.id, "Salvatore", panel)

        assert done.status is EventKind.EXECUTED
        assert done.events[-1].data == {
            "accepted": False,
            "code": "level_low",
            "reason": "livello basso",
        }

    async def test_the_second_approval_runs_nothing(self, queue):
        """[SEC] Approved twice: 409 the second time, and one press."""
        proposal = await proposed(queue)
        panel = FakePanel()
        await queue.approve(proposal.id, "Salvatore", panel)

        with pytest.raises(ConflictError):
            await queue.approve(proposal.id, "Salvatore", panel)

        assert len(panel.pressed) == 1

    async def test_two_approvals_at_once_press_once(self, queue, log):
        """[SEC] Two requests read "proposed" together: the log lets one decide.

        WHY: both pass the check on the status before either writes. Only
        the uniqueness of the decision, in the table, stops the second.
        """
        proposal = await proposed(queue)
        panel = FakePanel()

        results = await asyncio.gather(
            queue.approve(proposal.id, "Anna", panel),
            queue.approve(proposal.id, "Bruno", panel),
            return_exceptions=True,
        )

        assert len(panel.pressed) == 1
        assert sum(isinstance(r, ConflictError) for r in results) == 1
        assert [e.kind for e in log.events].count(EventKind.APPROVED) == 1

    async def test_a_rejected_proposal_never_runs(self, queue):
        """[SEC] Rejected, then approved: 409 and no press."""
        proposal = await proposed(queue)
        await queue.reject(proposal.id, "Salvatore", "prima controllo TT5a")
        panel = FakePanel()

        with pytest.raises(ConflictError):
            await queue.approve(proposal.id, "Salvatore", panel)

        assert panel.pressed == []

    async def test_a_blocked_proposal_cannot_be_approved(self, queue):
        """[SEC] The guardrail said no: no approval brings it back."""
        proposal = await queue.propose(
            "set_temperature", {"vessel": "FERM", "celsius": 80.0}, Actor.MCP, "x", ""
        )
        panel = FakePanel()

        with pytest.raises(ConflictError):
            await queue.approve(proposal.id, "Salvatore", panel)

        assert panel.pressed == []

    async def test_an_unknown_proposal_is_not_found(self, queue):
        """[EC] 404, and nothing pressed."""
        panel = FakePanel()

        with pytest.raises(NotFoundError):
            await queue.approve(uuid4(), "Salvatore", panel)

        assert panel.pressed == []

    async def test_a_plant_that_does_not_answer_is_a_failed_execution(self, queue):
        """[EC] Past the timeout: execution failed, written, and no second try."""
        proposal = await proposed(queue)

        done = await queue.approve(proposal.id, "Salvatore", FakePanel(hangs=True))

        assert done.status is EventKind.EXECUTION_FAILED
        assert "0.05 s" in done.events[-1].data["error"]
        with pytest.raises(ConflictError):
            await queue.approve(proposal.id, "Salvatore", FakePanel())

    async def test_a_plant_out_of_reach_is_a_failed_execution(self, queue):
        """[EC] The adapter cannot reach the plant: written as such."""
        proposal = await proposed(queue)
        panel = FakePanel(raises=ServiceUnavailableError("plant"))

        done = await queue.approve(proposal.id, "Salvatore", panel)

        assert done.status is EventKind.EXECUTION_FAILED
        assert done.events[-1].data == {"error": "Service temporarily unavailable"}

    async def test_each_event_has_the_simulated_time_of_its_moment(self, queue, clock):
        """[HP] Rule 5: every record carries the simulated time."""
        proposal = await proposed(queue)
        clock.time = 4000.0

        done = await queue.approve(proposal.id, "Salvatore", FakePanel())

        assert [e.sim_time_s for e in done.events] == [3600.0, 4000.0, 4000.0]


class TestReject:
    async def test_records_who_and_why(self, queue):
        """[HP] proposed, rejected: the brewer's name and reason are written."""
        proposal = await proposed(queue)

        done = await queue.reject(proposal.id, "Salvatore", "prima controllo TT5a")

        assert done.status is EventKind.REJECTED
        rejected = done.events[-1]
        assert (rejected.actor, rejected.by) == (Actor.USER, "Salvatore")
        assert rejected.data == {"reason": "prima controllo TT5a"}

    async def test_an_executed_proposal_cannot_be_rejected(self, queue):
        """[EC] Too late: 409."""
        proposal = await proposed(queue)
        await queue.approve(proposal.id, "Salvatore", FakePanel())

        with pytest.raises(ConflictError):
            await queue.reject(proposal.id, "Salvatore", "")


class TestRead:
    async def test_get_returns_the_whole_history(self, queue):
        """[HP] Every event, oldest first."""
        proposal = await proposed(queue)
        await queue.reject(proposal.id, "Salvatore", "")

        found = await queue.get(proposal.id)

        assert [e.kind for e in found.events] == [
            EventKind.PROPOSED,
            EventKind.REJECTED,
        ]

    async def test_get_unknown_is_not_found(self, queue):
        """[EC] 404."""
        with pytest.raises(NotFoundError):
            await queue.get(uuid4())

    async def test_page_shows_the_newest_first(self, queue):
        """[HP] The last proposal at the top of the list."""
        first = await proposed(queue)
        second = await proposed(queue, "reset", {})

        page = await queue.page(limit=10, offset=0)

        assert [p.id for p in page] == [second.id, first.id]
