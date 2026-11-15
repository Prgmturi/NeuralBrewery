from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from neuralbrewery.core.approvals.schemas import Actor, PastDecision, Receipt


@runtime_checkable
class ProposalInbox(Protocol):
    """The box where agents and the MCP server drop their proposals.

    It only takes: nothing here approves, rejects or reaches the plant.
    """

    async def propose(
        self,
        command: str,
        arguments: Mapping[str, Any],
        actor: Actor,
        by: str,
        why: str,
    ) -> Receipt:
        """Check the proposal against the panel and queue it, or block it.

        Out of limits is no error: the receipt says "blocked" and why.
        """
        ...


@runtime_checkable
class DecisionReader(Protocol):
    """The brewer's decisions on the agent's past proposals: its memory.

    It only reads: nothing here proposes, approves or rejects. Only the
    proposals of the agent come back: the why of an MCP proposal is written
    by anybody who reaches /mcp, and an agent that proposes must not read
    untrusted text.
    """

    async def recent(self, limit: int) -> list[PastDecision]:
        """The agent's proposals, the newest first, at most limit.

        Raises ServiceUnavailableError when the queue cannot be read.
        """
        ...
