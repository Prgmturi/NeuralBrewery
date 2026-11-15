"""Who acts on a proposal, and what the proposer gets back. Plain Python.

No pydantic: the domain of the approvals imports these names, and loads
no framework.
"""

from dataclasses import dataclass
from enum import StrEnum
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
