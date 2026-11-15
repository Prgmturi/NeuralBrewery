import secrets
from typing import Annotated

from fastapi import Depends, Header, Request

from neuralbrewery.core.config import ApprovalSettings
from neuralbrewery.core.database.dependencies import get_db_manager
from neuralbrewery.core.database.protocols import DatabaseProvider
from neuralbrewery.core.exceptions import UnauthorizedError
from neuralbrewery.core.plant.dependencies import PlantReaderDep
from neuralbrewery.features.approvals.api.clock import PlantClock
from neuralbrewery.features.approvals.api.executor import EXECUTOR
from neuralbrewery.features.approvals.domain.protocols import Panel, ProposalLog
from neuralbrewery.features.approvals.domain.service import ApprovalQueue
from neuralbrewery.features.approvals.persistence.repository import SqlProposalLog

TOKEN_HEADER = "X-Approval-Token"


def require_approval_token(
    request: Request,
    token: Annotated[str | None, Header(alias=TOKEN_HEADER)] = None,
) -> None:
    """401 unless the request carries APPROVAL_TOKEN.

    An empty APPROVAL_TOKEN matches nothing: nobody approves. The comparison
    takes the same time however much of the token is right. The token is
    never logged, and never reaches the MCP tools or the agents.
    """
    settings: ApprovalSettings = request.app.state.settings.approvals
    expected = settings.token.get_secret_value()
    if (
        not expected
        or token is None
        or not secrets.compare_digest(token.encode(), expected.encode())
    ):
        raise UnauthorizedError(
            "Approval token missing or wrong",
            headers={"WWW-Authenticate": f'ApprovalToken header="{TOKEN_HEADER}"'},
        )


def get_proposal_log(
    db: Annotated[DatabaseProvider, Depends(get_db_manager)],
) -> ProposalLog:
    """The log on Postgres: each event in a transaction of its own."""
    return SqlProposalLog(db.session_factory)


def get_queue(
    log: Annotated[ProposalLog, Depends(get_proposal_log)], reader: PlantReaderDep
) -> ApprovalQueue:
    return ApprovalQueue(log, PlantClock(reader))


def get_executor(request: Request) -> Panel:
    return EXECUTOR.get(request.app.state)


QueueDep = Annotated[ApprovalQueue, Depends(get_queue)]
ExecutorDep = Annotated[Panel, Depends(get_executor)]
BrewerOnly = Depends(require_approval_token)
