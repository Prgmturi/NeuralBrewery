"""The bodies the brewer sends."""

from pydantic import BaseModel, ConfigDict, Field

from neuralbrewery.features.approvals.domain.proposal import BY_MAX_LENGTH


class ApproveRequest(BaseModel):
    """Who approves: written in the audit as declared, not checked."""

    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, max_length=BY_MAX_LENGTH)


class RejectRequest(BaseModel):
    """Who rejects, and why: both written in the audit."""

    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, max_length=BY_MAX_LENGTH)
    reason: str = Field(default="", max_length=2000)
