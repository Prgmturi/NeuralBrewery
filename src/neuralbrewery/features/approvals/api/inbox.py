"""The ProposalInbox port on the queue: propose, and nothing else.

The MCP server and the agent endpoint get this, never the queue: it
holds no panel, and ApprovalQueue.approve() needs one, so through here
nothing is approved or pressed.
"""

from collections.abc import Callable, Mapping
from typing import Any

from neuralbrewery.core.approvals.schemas import Actor, Receipt
from neuralbrewery.core.database.protocols import DatabaseProvider
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.features.approvals.api.clock import PlantClock
from neuralbrewery.features.approvals.domain.protocols import ProposalLog
from neuralbrewery.features.approvals.domain.service import ApprovalQueue
from neuralbrewery.features.approvals.persistence.repository import SqlProposalLog


def database_log(database: Callable[[], DatabaseProvider]) -> Callable[[], ProposalLog]:
    """The log on the database of the app, found when a proposal arrives.

    The inbox is built with the app; the database opens later, in the
    lifespan.
    """
    return lambda: SqlProposalLog(database().session_factory)


class QueueInbox:
    def __init__(self, log: Callable[[], ProposalLog], reader: PlantReader) -> None:
        self._log = log
        self._reader = reader

    async def propose(
        self,
        command: str,
        arguments: Mapping[str, Any],
        actor: Actor,
        by: str,
        why: str,
    ) -> Receipt:
        queue = ApprovalQueue(self._log(), PlantClock(self._reader))
        proposal = await queue.propose(command, arguments, actor, by, why)
        return Receipt(proposal.id, proposal.status.value, proposal.blocked_reason)
