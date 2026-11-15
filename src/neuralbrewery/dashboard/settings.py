"""Where the dashboard finds the API, and the token it approves with."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DashboardSettings(BaseSettings):
    """Read from the environment, or from .env when the page runs on the host.

    compose.yaml sets both for its dashboard service. The token is the
    brewer's: never written in the code, never shown on the page, never
    logged. Empty, the API refuses every approval with 401, and the page
    shows it.
    """

    model_config = SettingsConfigDict(
        env_prefix="DASHBOARD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_url: str = "http://localhost:8000"
    approval_token: SecretStr = SecretStr("")
