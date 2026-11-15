from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from neuralbrewery.core.config.app import AppSettings
from neuralbrewery.core.config.approvals import ApprovalSettings
from neuralbrewery.core.config.auth_cookie import AuthCookieSettings
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.config.database import DatabaseSettings
from neuralbrewery.core.config.keycloak import KeycloakSettings
from neuralbrewery.core.config.plant import PlantSettings
from neuralbrewery.core.config.production import production_problems
from neuralbrewery.core.config.server import ServerSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    approvals: ApprovalSettings = Field(default_factory=ApprovalSettings)
    auth_cookie: AuthCookieSettings = Field(default_factory=AuthCookieSettings)
    claude: ClaudeSettings = Field(default_factory=ClaudeSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    keycloak: KeycloakSettings = Field(default_factory=KeycloakSettings)
    plant: PlantSettings = Field(default_factory=PlantSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)

    @model_validator(mode="after")
    def refuse_development_values_outside_development(self) -> "Settings":
        # Staging too: it is reached from outside and often holds real data.
        # All problems in one error: a deploy should not need one restart
        # per mistake
        if not self.app.is_development:
            problems = production_problems(
                self.app,
                self.auth_cookie,
                self.database,
                self.keycloak,
                self.server,
                self.plant,
                self.approvals,
            )
            if problems:
                raise ValueError(
                    f"refusing to start in {self.app.environment}:\n"
                    + "\n".join(f"- {problem}" for problem in problems)
                )
        return self


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


__all__ = [
    "Settings",
    "AppSettings",
    "ApprovalSettings",
    "AuthCookieSettings",
    "ClaudeSettings",
    "DatabaseSettings",
    "KeycloakSettings",
    "PlantSettings",
    "ServerSettings",
    "get_settings",
]
