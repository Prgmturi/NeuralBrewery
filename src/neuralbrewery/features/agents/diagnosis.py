"""What the plant agent answers, and how a run went.

The diagnosis is structured so that code can grade it, with no LLM as a
judge: which component, a fault of measure or of process, whether the data
are enough, and a command among the buttons of the panel, or none.
"""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

from neuralbrewery.core.plant.schemas import Proposal


class _Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)


class FaultType(StrEnum):
    MEASUREMENT = "measurement"  # the instrument lies: the plant is fine
    PROCESS = "process"  # the plant is faulty: the instruments tell the truth


class Diagnosis(_Frozen):
    component: str = Field(min_length=1)  # a tag, or a route
    fault_type: FaultType
    confirmed: bool  # the data are enough to name the cause
    explanation: str  # for the brewer, in Italian
    checks: tuple[str, ...]  # by hand, for the brewer
    proposal: Proposal | None  # None: the checks come first


class Outcome(StrEnum):
    DIAGNOSED = "diagnosed"
    NO_DIAGNOSIS = "no_diagnosis"  # an answer in text, or no answer at all
    INVALID_DIAGNOSIS = "invalid_diagnosis"  # handed in, outside the schema
    REFUSED = "refused"  # the safety classifiers declined, fallback included


class Step(_Frozen):
    """One call of the model, or one tool, as the trace recorded it."""

    kind: Literal["model", "tool"]
    name: str  # the model, or the tool
    stop_reason: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0  # read from the prompt cache
    arguments: str = ""  # of a tool, as datapizza writes them
    result: str = ""  # of a tool


class DiagnosisRun(_Frozen):
    outcome: Outcome
    diagnosis: Diagnosis | None
    detail: str  # why there is no diagnosis, in words
    steps: tuple[Step, ...]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def input_tokens(self) -> int:
        return sum(step.input_tokens for step in self.steps)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def output_tokens(self) -> int:
        return sum(step.output_tokens for step in self.steps)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cached_tokens(self) -> int:
        return sum(step.cached_tokens for step in self.steps)
