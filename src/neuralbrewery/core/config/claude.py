from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ClaudeSettings(BaseSettings):
    """The model of the agents and how much each call may spend.

    The key is read from ANTHROPIC_API_KEY, the name the Anthropic tools
    use; everything else from CLAUDE_*. Not ANTHROPIC_MODEL: Claude Code
    and other tools export it, and it would change the model of the app
    without anyone noticing.
    """

    model_config = SettingsConfigDict(
        env_prefix="CLAUDE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_by_name=True,
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    # SecretStr: repr() and model_dump() show stars, get_secret_value() the key
    api_key: SecretStr = Field(
        default=SecretStr(""),
        validation_alias="ANTHROPIC_API_KEY",
        description="Anthropic API key. Empty: the agents cannot run",
    )
    model: str = Field(default="claude-sonnet-5-5", description="Model of the agents")
    # Thinking and answer share this budget: the default of datapizza, 2048,
    # can end a diagnosis half way
    max_tokens: int = Field(default=16000, ge=1, description="Tokens per call")
    effort: Literal["low", "medium", "high", "xhigh", "max"] = Field(
        default="high", description="How much the model thinks; high for a diagnosis"
    )
