"""A datapizza client that answers from a script: the agent's loop, no network.

Each call takes the next reply of the script, and the last one repeats.
A reply is built when the call arrives, from the tools the agent offers,
as a real model would see them.
"""

from collections.abc import Callable, Mapping
from typing import Any
from uuid import UUID

from datapizza.core.clients import Client, ClientResponse
from datapizza.core.clients.models import TokenUsage
from datapizza.tools import Tool
from datapizza.type import FunctionCallBlock, TextBlock

from neuralbrewery.core.approvals.schemas import Actor, PastDecision, Receipt
from neuralbrewery.core.manuals.schemas import ManualPassage

Reply = Callable[[dict[str, Tool]], ClientResponse]

# What every scripted call costs: easy to add up in a test
USAGE = {"prompt_tokens": 100, "completion_tokens": 20, "cached_tokens": 50}


class ScriptedClient(Client):
    def __init__(self, *replies: Reply) -> None:
        super().__init__(model_name="scripted", system_prompt="")
        self._replies = list(replies)
        self.calls: list[dict[str, Any]] = []  # the arguments of each call

    async def _a_invoke(self, **kwargs: Any) -> ClientResponse:
        self.calls.append(kwargs)
        reply = self._replies.pop(0) if len(self._replies) > 1 else self._replies[0]
        return reply({tool.name: tool for tool in kwargs["tools"]})

    def first_message(self) -> str:
        """The text the agent opened the conversation with."""
        return "\n".join(block.content for block in self.calls[0]["input"])

    def _invoke(self, **kwargs: Any) -> ClientResponse:
        raise NotImplementedError

    def _stream_invoke(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _a_stream_invoke(self, **kwargs: Any) -> Any:
        raise NotImplementedError

    def _structured_response(self, **kwargs: Any) -> ClientResponse:
        raise NotImplementedError

    async def _a_structured_response(self, **kwargs: Any) -> ClientResponse:
        raise NotImplementedError

    def _convert_tool_choice(self, tool_choice: Any) -> Any:
        return tool_choice


def call(name: str, **arguments: Any) -> Reply:
    """The model asks for one tool."""

    def reply(tools: dict[str, Tool]) -> ClientResponse:
        block = FunctionCallBlock(
            id=f"call-{name}", name=name, arguments=arguments, tool=tools[name]
        )
        return ClientResponse(
            content=[block], stop_reason="tool_use", usage=TokenUsage(**USAGE)
        )

    return reply


def together(*replies: Reply) -> Reply:
    """Several tools in one turn, as a model may ask them in parallel."""

    def reply(tools: dict[str, Tool]) -> ClientResponse:
        made = [each(tools) for each in replies]
        return ClientResponse(
            content=[block for response in made for block in response.content],
            stop_reason="tool_use",
            usage=TokenUsage(**USAGE),
        )

    return reply


def say(text: str) -> Reply:
    """The model answers in text, and calls nothing."""

    def reply(tools: dict[str, Tool]) -> ClientResponse:
        return ClientResponse(
            content=[TextBlock(content=text)],
            stop_reason="end_turn",
            usage=TokenUsage(**USAGE),
        )

    return reply


def refuse(stop_reason: str = "refusal") -> Reply:
    """The safety classifiers decline: nothing comes back.

    "refusal" is Claude's stop reason; "content_filter" is the finish reason
    of the APIs that copy OpenAI's, Gemini's included.
    """

    def reply(tools: dict[str, Tool]) -> ClientResponse:
        return ClientResponse(content=[], stop_reason=stop_reason, usage=TokenUsage())

    return reply


DIAGNOSIS = {
    "component": "TT5a",
    "fault_type": "measurement",
    "confirmed": True,
    "explanation": "TT5a legge 2 °C più di TT5b e dell'iSpindel.",
    "checks": ["Confrontare TT5a con un termometro di riferimento"],
    "command": "set_temperature",
    "vessel": "FERM",
    "celsius": 21.0,
}


PROPOSAL_ID = UUID("6f1c2a5e-0000-4000-8000-000000000001")


class RecordingInbox:
    """The ProposalInbox port: records each proposal, answers as told."""

    def __init__(self, receipt: Receipt | None = None) -> None:
        self.proposals: list[tuple[str, dict[str, Any], Actor, str, str]] = []
        self._receipt = receipt or Receipt(PROPOSAL_ID, "proposed")

    async def propose(
        self,
        command: str,
        arguments: Mapping[str, Any],
        actor: Actor,
        by: str,
        why: str,
    ) -> Receipt:
        self.proposals.append((command, dict(arguments), actor, by, why))
        return self._receipt


REJECTED_RESET = PastDecision(
    command="reset",
    arguments={},
    why="TT1 legge di nuovo bene: resta solo il blocco del controllore.",
    status="rejected",
    reason="TT1 ha un contatto intermittente: va sostituita prima di riarmare",
)


class FakeDecisions:
    """The DecisionReader port: the decisions given, or the error given."""

    def __init__(
        self, *decisions: PastDecision, raises: Exception | None = None
    ) -> None:
        self.asked: list[int] = []  # the limit of each read
        self._decisions = list(decisions)
        self._raises = raises

    async def recent(self, limit: int) -> list[PastDecision]:
        self.asked.append(limit)
        if self._raises is not None:
            raise self._raises
        return self._decisions[:limit]


F11 = ManualPassage(
    document="vfd-siemens-v20-getting-started",
    product="Siemens SINAMICS V20",
    tags=("M1",),
    page=55,
    text="Fault code list\n| Fault | Description |\n| F11 | Motor overtemperature |",
)


class FakeManuals:
    """The ManualSearch port: the passages given, whatever is asked."""

    def __init__(self, *passages: ManualPassage, tags: tuple[str, ...] = ("M1",)):
        self.asked: list[tuple[str, str]] = []  # query and tag of each search
        self._passages = list(passages)
        self._tags = frozenset(tags)

    def tags(self) -> frozenset[str]:
        return self._tags

    def search(self, query: str, tag: str = "", limit: int = 3) -> list[ManualPassage]:
        self.asked.append((query, tag))
        return self._passages[:limit]
