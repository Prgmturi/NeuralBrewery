from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """Which provider the agents run on.

    claude, the default, reads ClaudeSettings; openai_compat reads
    OpenAICompatSettings. Only the key of the chosen provider counts: with
    it empty there is no agent, and its endpoint answers 503.
    """

    model_config = SettingsConfigDict(
        env_prefix="AGENT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        hide_input_in_errors=True,
    )

    provider: Literal["claude", "openai_compat"] = Field(
        default="claude",
        description="claude, or openai_compat: an API that copies OpenAI's",
    )
