"""Who acts on a proposal, what the proposer gets back, what the agent recalls.

Plain Python. No pydantic: the domain of the approvals imports these
names, and loads no framework.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from typing import Any
from uuid import UUID


class Actor(StrEnum):
    """Who wrote an event of a proposal."""

    USER = "user"  # the brewer, with the approval token
    AGENT = "agent"  # an agent of the app, such as the plant agent
    MCP = "mcp"  # a client of the MCP server, such as Claude Code
    EXECUTOR = "executor"  # the code that presses the approved button


@dataclass(frozen=True)
class Receipt:
    """What a proposer learns: the id, and whether the proposal entered.

    status is "proposed" (waiting for the brewer) or "blocked" (out of
    limits: reason says why). No real time: a model reads it (rule 5).
    """

    proposal_id: UUID
    status: str
    reason: str = ""


@dataclass(frozen=True)
class PastDecision:
    """One of the agent's past proposals, and what became of it.

    The memory of the plant agent: what the brewer decided, and what the
    controller answered. No time, real or simulated (rule 5): a restart
    sets the simulated clock back to zero, so the time of a past brew says
    nothing about now. No names either: who proposed is always the agent.
    """

    command: str
    arguments: Mapping[str, Any]
    why: str  # the explanation of the diagnosis that proposed it
    # The last event: proposed, blocked, approved, rejected, executed or
    # execution_failed
    status: str
    reason: str = ""  # why the brewer rejected it, or the guardrail blocked it
    answer: str = ""  # the controller's code and reason, or why it said nothing
