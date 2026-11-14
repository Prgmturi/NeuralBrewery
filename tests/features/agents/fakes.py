"""A datapizza client that answers from a script: the agent's loop, no network.

Each call takes the next reply of the script, and the last one repeats.
A reply is built when the call arrives, from the tools the agent offers,
as a real model would see them.
"""

from collections.abc import Callable
from typing import Any

from datapizza.core.clients import Client, ClientResponse
from datapizza.core.clients.models import TokenUsage
from datapizza.tools import Tool
from datapizza.type import FunctionCallBlock, TextBlock

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


def refuse() -> Reply:
    """The safety classifiers decline: nothing comes back."""

    def reply(tools: dict[str, Tool]) -> ClientResponse:
        return ClientResponse(content=[], stop_reason="refusal", usage=TokenUsage())

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
