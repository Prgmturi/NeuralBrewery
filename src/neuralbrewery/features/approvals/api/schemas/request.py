"""The bodies the brewer sends."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from neuralbrewery.features.approvals.domain.proposal import BY_MAX_LENGTH


class ProposeRequest(BaseModel):
    """A button the brewer proposes, as propose_action of the MCP server takes it.

    The guardrail checks command and arguments, as for any proposal: out of
    limits the proposal is blocked, not refused with an error.
    """

    model_config = ConfigDict(extra="forbid")

    command: str = Field(min_length=1, max_length=100)
    arguments: dict[str, Any] = Field(default_factory=dict)
    why: str = Field(default="", max_length=2000)
    by: str = Field(min_length=1, max_length=BY_MAX_LENGTH)


class ApproveRequest(BaseModel):
    """Who approves: written in the audit as declared, not checked."""

    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, max_length=BY_MAX_LENGTH)


class RejectRequest(BaseModel):
    """Who rejects, and why: both written in the audit."""

    model_config = ConfigDict(extra="forbid")

    by: str = Field(min_length=1, max_length=BY_MAX_LENGTH)
    reason: str = Field(default="", max_length=2000)
