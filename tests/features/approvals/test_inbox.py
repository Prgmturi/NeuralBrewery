"""Tests for the inbox: how the MCP server and the agents propose.

Module under test: src/neuralbrewery/features/approvals/api/inbox.py
Layer: Edge of the feature; the log in memory, the plant real

WHY these tests exist: the inbox is all an agent or an MCP client holds
of the queue. A proposal through it is checked by the guardrail and
written with who sent it and the simulated time; the receipt says
whether it entered, and why not.
"""

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.approvals.protocols import ProposalInbox
from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.features.approvals.api.inbox import QueueInbox, database_log
from neuralbrewery.features.approvals.domain.proposal import EventKind
from neuralbrewery.features.approvals.persistence.repository import SqlProposalLog
from tests.features.approvals.fakes import InMemoryProposalLog


def inbox_on(log: InMemoryProposalLog) -> QueueInbox:
    return QueueInbox(lambda: log, InProcessPlant(brew_day()))


async def test_a_proposal_within_limits_waits_for_the_brewer(log):
    """[HP] Receipt "proposed"; the event names the agent and its reason."""
    receipt = await inbox_on(log).propose(
        "set_temperature",
        {"vessel": "HLT", "celsius": 70.0},
        Actor.AGENT,
        "plant_agent",
        "acqua per l'impasto",
    )

    assert (receipt.status, receipt.reason) == ("proposed", "")
    [event] = log.events
    assert event.proposal_id == receipt.proposal_id
    assert (event.kind, event.actor, event.by) == (
        EventKind.PROPOSED,
        Actor.AGENT,
        "plant_agent",
    )
    assert event.sim_time_s == 0.0


async def test_out_of_limits_the_receipt_says_why(log):
    """[SEC] Blocked: the reason goes back to whoever proposed."""
    receipt = await inbox_on(log).propose(
        "set_temperature", {"vessel": "HLT", "celsius": 95.0}, Actor.MCP, "mcp", ""
    )

    assert receipt.status == "blocked"
    assert "85" in receipt.reason


def test_the_inbox_is_the_port_of_the_core(log):
    """[HP] What bootstrap.py hands to the MCP server and to the agents."""
    assert isinstance(inbox_on(log), ProposalInbox)


def test_outside_tests_the_log_is_the_table(mock_db_provider):
    """[HP] Found when a proposal arrives, on the sessions of the app."""
    assert isinstance(database_log(lambda: mock_db_provider)(), SqlProposalLog)
