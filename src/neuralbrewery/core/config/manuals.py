from pathlib import Path
from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ManualsSettings(BaseSettings):
    """The manuals of the components, searched by the plant agent.

    Off by default: the agent has the tools it had before, and the app
    starts without the folder. On, the folder must hold the text of the
    manuals (scripts/extract_manuals.py writes it): without it the app
    does not start, rather than run an agent that finds nothing.
    """

    model_config = SettingsConfigDict(
        env_prefix="MANUALS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    enabled: bool = Field(
        default=False,
        description="Give the plant agent the search over the manuals",
    )
    # Relative to where the app starts: the root of the repository, or
    # /app in the image, which holds the same folder
    folder: Path = Field(
        default=Path("data/manuals/text"),
        description="The text of the manuals, one <id>.md per document",
    )

    @model_validator(mode="after")
    def the_text_is_there_when_enabled(self) -> Self:
        if self.enabled and not any(self.folder.glob("*.md")):
            raise ValueError(
                f"MANUALS_ENABLED is true, but MANUALS_FOLDER ({self.folder}) "
                "holds no text of the manuals (*.md). Run "
                "python scripts/extract_manuals.py from the root of the "
                "repository, point MANUALS_FOLDER at the text, or switch "
                "MANUALS_ENABLED off"
            )
        return self
