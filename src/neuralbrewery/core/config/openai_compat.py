from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/"


class OpenAICompatSettings(BaseSettings):
    """The second provider of the agents: any API that copies OpenAI's.

    Gemini on its free tier by default; Groq or a local model take only
    another address, model and key. The model is pinned: an alias such as
    gemini-flash-lite-latest moves to a new model under the evals.
    """

    model_config = SettingsConfigDict(
        env_prefix="OPENAI_COMPAT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    base_url: str = Field(default=GEMINI, description="Address of the API")
    model: str = Field(default="gemini-3.5-flash-lite", description="Model")
    # SecretStr: repr() and model_dump() show stars, get_secret_value() the key
    api_key: SecretStr = Field(
        default=SecretStr(""),
        description="Key of the API. Empty: no agent on this provider",
    )
