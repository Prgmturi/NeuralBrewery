"""Tests for the Claude adapter.

Under test: src/neuralbrewery/adapters/claude/client.py
No network: building the client makes no call, and the calls go to an
httpx transport that answers in the test.

WHY these tests exist: the step-1 trial of M5 (docs/decisioni.md) found
what datapizza leaves to the caller with Claude: max_tokens falls back to
2048, effort is not set, a forced tool_choice is a 400. These arguments are
the whole fix, so a lost one would change every diagnosis without a sign.
"""

import httpx
import pytest
from anthropic import AsyncAnthropic
from datapizza.clients.anthropic import AnthropicClient

from neuralbrewery.adapters.claude.client import (
    FALLBACK_BETA,
    ClaudeClient,
    create_client,
    generation_args,
)
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.exceptions import ExternalServiceError, ServiceUnavailableError


def test_the_client_takes_model_and_key_from_the_settings():
    """[HP] One client per model; the key goes to the SDK and nowhere else."""
    client = create_client(
        ClaudeSettings(api_key="sk-ant-test", model="claude-opus-5-5")
    )

    assert isinstance(client, AnthropicClient)
    assert client.model_name == "claude-opus-5-5"
    assert client.api_key == "sk-ant-test"


def test_every_call_carries_tokens_effort_fallback_and_cache():
    """[HP] What datapizza would otherwise leave out or get wrong."""
    args = generation_args(ClaudeSettings(max_tokens=9000, effort="medium"))

    assert args == {
        "max_tokens": 9000,
        "output_config": {"effort": "medium"},
        "extra_headers": {"anthropic-beta": FALLBACK_BETA},
        "extra_body": {
            "fallbacks": "default",
            "cache_control": {"type": "ephemeral"},
        },
    }


def test_no_call_forces_a_tool():
    """[EC] A forced tool_choice is a 400 on the current Claude models."""
    assert "tool_choice" not in generation_args(ClaudeSettings())


def claude_answering(handler) -> ClaudeClient:
    """The client of the app, its HTTP answered by handler: no network, no retry."""
    client = create_client(ClaudeSettings(api_key="sk-ant-test"))
    client.a_client = AsyncAnthropic(
        api_key="sk-ant-test",
        base_url="http://anthropic.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )
    return client


def status(code: int):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            code, json={"type": "error", "error": {"type": "x", "message": "no"}}
        )

    return handler


def raising(error: Exception):
    def handler(request: httpx.Request) -> httpx.Response:
        raise error

    return handler


ANSWER = {
    "id": "msg_1",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-5-5",
    "content": [{"type": "text", "text": "ciao"}],
    "stop_reason": "end_turn",
    "stop_sequence": None,
    "usage": {
        "input_tokens": 3,
        "output_tokens": 1,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0,
    },
}


class TestErrorsOfTheApi:
    """ADR 0006: the SDK's errors become the app's, so the API answers 503 or 502.

    WHY: served by the API, the agent raised the SDK's own exceptions, which
    the exception handlers do not know: every failure of Anthropic was a 500.
    """

    def test_the_client_of_the_app_translates(self):
        """[HP] create_client builds the subclass, still datapizza's client."""
        client = create_client(ClaudeSettings())

        assert isinstance(client, ClaudeClient)
        assert isinstance(client, AnthropicClient)

    async def test_an_answer_goes_through(self):
        """[HP] 200: datapizza's response, unchanged."""
        client = claude_answering(lambda request: httpx.Response(200, json=ANSWER))

        response = await client.a_invoke("ciao", max_tokens=10)

        assert response.text == "ciao"

    @pytest.mark.parametrize(
        "error",
        [
            httpx.ConnectError("refused"),
            httpx.ReadTimeout("slow"),
        ],
        ids=["unreachable", "timeout"],
    )
    async def test_out_of_reach_is_503(self, error):
        """[EC] No answer at all: retry later."""
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await claude_answering(raising(error)).a_invoke("ciao", max_tokens=10)

        assert exc_info.value.details == {"service": "Claude"}

    @pytest.mark.parametrize("code", [429, 500, 529])
    async def test_busy_or_down_is_503(self, code):
        """[EC] Rate limited, an error of theirs, overloaded: retry later."""
        with pytest.raises(ServiceUnavailableError):
            await claude_answering(status(code)).a_invoke("ciao", max_tokens=10)

    @pytest.mark.parametrize("code", [400, 401, 404])
    async def test_a_request_they_refuse_is_502(self, code):
        """[EC] A bad request, a wrong key, an unknown model: no retry helps."""
        with pytest.raises(ExternalServiceError) as exc_info:
            await claude_answering(status(code)).a_invoke("ciao", max_tokens=10)

        assert str(code) in exc_info.value.message
