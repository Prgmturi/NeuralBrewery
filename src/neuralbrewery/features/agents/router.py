from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from neuralbrewery.core.approvals.protocols import ProposalInbox
from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.exceptions import ServiceUnavailableError
from neuralbrewery.core.state import StateKey
from neuralbrewery.features.agents.diagnosis import DiagnosisRun
from neuralbrewery.features.agents.plant_agent import NAME, PlantAgent

# Set by bootstrap.py: the agent only when the chosen provider has a key, and
# always the name of that provider, for the 503 without it
PLANT_AGENT = StateKey[PlantAgent]("plant_agent")
AGENT_SERVICE = StateKey[str]("agent_service")
PROPOSAL_INBOX = StateKey[ProposalInbox]("proposal_inbox")

agents_router = APIRouter(prefix="/agents", tags=["Agents"])


def get_plant_agent(request: Request) -> PlantAgent:
    """503 when there is no agent: the key of the chosen provider is empty."""
    try:
        return PLANT_AGENT.get(request.app.state)
    except AttributeError as error:
        raise ServiceUnavailableError(AGENT_SERVICE.get(request.app.state)) from error


def get_proposal_inbox(request: Request) -> ProposalInbox:
    return PROPOSAL_INBOX.get(request.app.state)


class QueuedResponse(BaseModel):
    """The proposal of the diagnosis in the queue: waiting, or blocked and why."""

    proposal_id: UUID
    status: str
    reason: str


class DiagnosisResponse(BaseModel):
    run: DiagnosisRun  # the diagnosis, every step and its tokens
    queued: QueuedResponse | None  # None: the diagnosis proposed no command


@agents_router.post("/plant/diagnose", summary="Diagnose the plant now")
async def diagnose_plant(
    agent: Annotated[PlantAgent, Depends(get_plant_agent)],
    inbox: Annotated[ProposalInbox, Depends(get_proposal_inbox)],
) -> DiagnosisResponse:
    """The plant agent reads the plant and diagnoses what is wrong now.

    Its proposal, if it makes one, goes into the queue as from the agent,
    through the guardrail: the brewer approves it at /approvals. One call
    of the model per step, up to twelve: a few cents on claude-sonnet-5-5,
    nothing on the free tier of Gemini. 503 when the provider cannot be
    reached, is over its limits, or has no key; 502 when it refuses the
    request or its answer cannot be used.
    """
    run = await agent.diagnose()
    queued = None
    if run.diagnosis is not None and run.diagnosis.proposal is not None:
        proposal = run.diagnosis.proposal
        receipt = await inbox.propose(
            proposal.command.value,
            proposal.arguments(),
            Actor.AGENT,
            NAME,
            run.diagnosis.explanation,
        )
        queued = QueuedResponse(
            proposal_id=receipt.proposal_id,
            status=receipt.status,
            reason=receipt.reason,
        )
    return DiagnosisResponse(run=run, queued=queued)
