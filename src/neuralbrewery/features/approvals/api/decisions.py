"""The DecisionReader port on the queue: the memory of the plant agent.

The agent gets this, never the queue. Through here it reads what the
brewer decided on its own proposals, and nothing else: no MCP proposal,
whose why anybody reaching /mcp writes, and no time (AGENTS.md, rule 5).
It holds no panel, and calls nothing that writes.
"""

from collections.abc import Callable

from sqlalchemy.exc import SQLAlchemyError

from neuralbrewery.core.approvals.schemas import Actor, PastDecision
from neuralbrewery.core.exceptions import ServiceUnavailableError
from neuralbrewery.features.approvals.domain.protocols import ProposalLog

SERVICE = "approval queue"


class QueueDecisions:
    def __init__(self, log: Callable[[], ProposalLog]) -> None:
        self._log = log

    async def recent(self, limit: int) -> list[PastDecision]:
        """Raises ServiceUnavailableError when the queue cannot be read.

        A lost connection comes from SQLAlchemy, or bare from the driver:
        asyncpg raises OSError when Postgres refuses it.
        """
        try:
            proposals = await self._log().page(limit, 0, actor=Actor.AGENT)
        except (SQLAlchemyError, OSError) as error:
            raise ServiceUnavailableError(SERVICE) from error
        return [proposal.decision() for proposal in proposals]
