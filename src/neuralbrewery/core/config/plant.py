from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PlantSettings(BaseSettings):
    """The simulated plant that lives in the process of the API, until M2.

    A restart builds a new plant from the same start: what happened before
    is gone, the queue of proposals stays in Postgres.
    """

    model_config = SettingsConfigDict(
        env_prefix="PLANT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # A failed check prints its input, which holds lines of .env: the
        # error would show their values, secrets included
        hide_input_in_errors=True,
    )

    start: Literal["brew_day", "fermentation"] = Field(
        default="brew_day",
        description="The named start of adapters/plant_sim/starts.py",
    )
    seed: int = Field(default=42, description="Same seed, same plant")
    # Off unless asked for: staging and production refuse it
    simulation_control: bool = Field(
        default=False,
        description="Expose the routes that move the time and inject faults",
    )
