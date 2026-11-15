"""The bodies the routes return: a proposal and its story."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ActionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    command: str
    arguments: dict[str, Any]


class ProposalEventResponse(BaseModel):
    """One step: who, as declared, and when, in simulated and in real time."""

    model_config = ConfigDict(from_attributes=True)

    seq: int
    kind: str
    actor: str
    by: str
    data: dict[str, Any]
    sim_time_s: float
    at: datetime


class ProposalResponse(BaseModel):
    """A proposal; its status is the kind of its last event.

    proposed waits for the brewer; blocked never entered the queue;
    executed means the controller answered, a refusal included (the data
    of the last event say which); execution_failed means it did not answer.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    action: ActionResponse
    why: str
    blocked_reason: str
    events: list[ProposalEventResponse]
