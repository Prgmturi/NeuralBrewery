from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from neuralbrewery.core.approvals.schemas import Actor, Receipt


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
