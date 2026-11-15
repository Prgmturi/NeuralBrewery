from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from neuralbrewery.core.database import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from neuralbrewery.features.approvals.api.dependencies import (
    BrewerOnly,
    ExecutorDep,
    QueueDep,
)
from neuralbrewery.features.approvals.api.schemas.request import (
    ApproveRequest,
    RejectRequest,
)
from neuralbrewery.features.approvals.api.schemas.response import ProposalResponse

approvals_router = APIRouter(prefix="/approvals", tags=["Approvals"])


@approvals_router.get("", summary="The queue of proposals")
async def list_proposals(
    queue: QueueDep,
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[ProposalResponse]:
    """Every proposal with its story, the newest first. Reading needs no token."""
    proposals = await queue.page(limit, offset)
    return [ProposalResponse.model_validate(proposal) for proposal in proposals]


@approvals_router.get("/{proposal_id}", summary="One proposal")
async def get_proposal(proposal_id: UUID, queue: QueueDep) -> ProposalResponse:
    return ProposalResponse.model_validate(await queue.get(proposal_id))


@approvals_router.post(
    "/{proposal_id}/approve",
    dependencies=[BrewerOnly],
    summary="Approve, and execute on the plant",
)
async def approve(
    proposal_id: UUID, payload: ApproveRequest, queue: QueueDep, executor: ExecutorDep
) -> ProposalResponse:
    """Needs X-Approval-Token. The executor presses the button at once.

    The answer holds the outcome: executed, with the controller's answer
    (a refusal of an interlock included), or execution_failed. 409 if the
    proposal is not waiting.
    """
    proposal = await queue.approve(proposal_id, payload.by, executor)
    return ProposalResponse.model_validate(proposal)


@approvals_router.post(
    "/{proposal_id}/reject", dependencies=[BrewerOnly], summary="Reject"
)
async def reject(
    proposal_id: UUID, payload: RejectRequest, queue: QueueDep
) -> ProposalResponse:
    """Needs X-Approval-Token. 409 if the proposal is not waiting."""
    proposal = await queue.reject(proposal_id, payload.by, payload.reason)
    return ProposalResponse.model_validate(proposal)
