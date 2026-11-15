from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApprovalSettings(BaseSettings):
    """Who may approve a proposal: whoever has this token.

    The token goes in the X-Approval-Token header of approve and reject. It
    never reaches the MCP tools, the agents or their prompts.
    """

    model_config = SettingsConfigDict(
        env_prefix="APPROVAL_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    # SecretStr: repr() and model_dump() show stars
    token: SecretStr = Field(
        default=SecretStr(""),
        description="Token of the brewer. Empty: nobody can approve",
    )
