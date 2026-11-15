"""Tests for the adapter of an API that copies OpenAI's: Gemini by default.

Under test: src/neuralbrewery/adapters/openai_compat/client.py
No network: building the client makes no call, and the calls go to an
httpx transport that answers in the test.

WHY these tests exist: the gate of M6 (docs/decisioni.md, "Secondo
fornitore") found that Gemini 3 refuses with a 400 a conversation whose tool
calls come back without their thought signature, and that datapizza drops
it: without the adapter the agent stops at its second call. Served by the
API, the errors of the SDK must answer 503 or 502 (ADR 0006), and the key
must stay out of everything the app writes.
"""

import json
from unittest.mock import MagicMock

import httpx
import pytest
from datapizza.clients.openai_like import OpenAILikeClient
from datapizza.tools import Tool
from openai import AsyncOpenAI

from neuralbrewery.adapters.openai_compat import client as adapter
from neuralbrewery.adapters.openai_compat.client import (
    SERVICE,
    OpenAICompatClient,
    create_client,
    generation_args,
)
from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.config.openai_compat import OpenAICompatSettings
from neuralbrewery.core.exceptions import ExternalServiceError, ServiceUnavailableError
from neuralbrewery.features.agents import plant_agent
from neuralbrewery.features.agents.diagnosis import DiagnosisRun, Outcome
from neuralbrewery.features.agents.plant_agent import PlantAgent
from tests.features.agents.fakes import DIAGNOSIS, FakeDecisions

KEY = "gm-secret-test-key"


def answering(handler) -> OpenAICompatClient:
    """The client of the app, its HTTP answered by handler: no network, no retry."""
    client = create_client(OpenAICompatSettings(api_key=KEY))
    client.a_client = AsyncOpenAI(
        api_key=KEY,
        base_url="http://compat.test/v1/",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )
    return client


def completion(finish_reason: str = "stop", **message) -> dict:
    """A chat completion, as the API answers it."""
    return {
        "id": "completion-1",
        "object": "chat.completion",
        "created": 0,
        "model": "gemini-3.5-flash-lite",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": None, **message},
                "finish_reason": finish_reason,
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
    }


def tool_call(name: str, arguments: str, call_id: str, signature: str = "") -> dict:
    """One tool call; Gemini signs the first of each answer."""
    call = {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": arguments},
    }
    if signature:
        call["extra_content"] = {"google": {"thought_signature": signature}}
    return call


def status(code: int, message: str = "no"):
    def handler(request: httpx.Request) -> httpx.Response:
        # Gemini wraps its errors in a list
        return httpx.Response(
            code, json=[{"error": {"code": code, "message": message}}]
        )

    return handler


def raising(error: Exception):
    def handler(request: httpx.Request) -> httpx.Response:
        raise error

    return handler


def answers(*bodies: dict):
    """One body per call, in order; the requests are kept, as JSON."""
    requests: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(json.loads(request.content))
        return httpx.Response(200, json=bodies[len(requests) - 1])

    return handler, requests


async def read_plant() -> str:
    """Legge l'impianto."""
    return "{}"


TOOLS = [Tool(read_plant)]


def test_the_client_takes_address_model_and_key_from_the_settings():
    """[HP] Any API that copies OpenAI's: three settings, the same code."""
    client = create_client(
        OpenAICompatSettings(
            api_key=KEY, model="llama-4-scout", base_url="https://groq.test/v1/"
        )
    )

    assert isinstance(client, OpenAILikeClient)
    assert client.model_name == "llama-4-scout"
    assert client.base_url == "https://groq.test/v1/"
    assert client.api_key == KEY


def test_every_call_carries_a_token_budget_and_nothing_of_claude():
    """[HP] No effort, no cache, no fallback: those are Claude's alone."""
    assert generation_args() == {"max_tokens": adapter.MAX_TOKENS}


class TestErrorsOfTheApi:
    """ADR 0006: the SDK's errors become the app's, so the API answers 503 or 502."""

    def test_the_client_of_the_app_translates(self):
        """[HP] create_client builds the subclass, still datapizza's client."""
        client = create_client(OpenAICompatSettings(api_key=KEY))

        assert isinstance(client, OpenAICompatClient)

    async def test_an_answer_goes_through(self):
        """[HP] 200: datapizza's response, unchanged."""
        handler, _ = answers(completion(content="ciao"))

        response = await answering(handler).a_invoke("ciao", max_tokens=10)

        assert response.text == "ciao"

    @pytest.mark.parametrize(
        "error",
        [httpx.ConnectError("refused"), httpx.ReadTimeout("slow")],
        ids=["unreachable", "timeout"],
    )
    async def test_out_of_reach_is_503(self, error):
        """[EC] No answer at all: retry later."""
        with pytest.raises(ServiceUnavailableError) as exc_info:
            await answering(raising(error)).a_invoke("ciao", max_tokens=10)

        assert exc_info.value.details == {"service": SERVICE}

    @pytest.mark.parametrize("code", [429, 500, 503])
    async def test_over_the_limits_or_down_is_503(self, code):
        """[EC] 429 is the free tier past 15 requests a minute: retry later."""
        with pytest.raises(ServiceUnavailableError):
            await answering(status(code)).a_invoke("ciao", max_tokens=10)

    @pytest.mark.parametrize("code", [400, 401, 404])
    async def test_a_request_they_refuse_is_502(self, code):
        """[EC] A bad request, a wrong key, a model gone: no retry helps."""
        with pytest.raises(ExternalServiceError) as exc_info:
            await answering(status(code)).a_invoke("ciao", max_tokens=10)

        assert str(code) in exc_info.value.message

    @pytest.mark.parametrize(
        "body",
        [
            completion("tool_calls", tool_calls=[tool_call("read_plant", "{no", "c1")]),
            completion("tool_calls", tool_calls=[tool_call("open_ev2", "{}", "c1")]),
            {**completion(), "choices": []},
        ],
        ids=["arguments-not-json", "unknown-tool", "no-choice"],
    )
    async def test_an_answer_that_cannot_be_used_is_502(self, body):
        """[EC] datapizza raises ValueError or IndexError on these: a 500 before."""
        handler, _ = answers(body)

        with pytest.raises(ExternalServiceError):
            await answering(handler).a_invoke("ciao", tools=TOOLS, max_tokens=10)


async def diagnose(handler) -> DiagnosisRun:
    plant = InProcessPlant(brew_day(seed=42))
    return await PlantAgent(
        plant, FakeDecisions(), answering(handler), generation_args()
    ).diagnose()


SUBMIT = json.dumps({**DIAGNOSIS, "command": None})


class TestThoughtSignatures:
    """Gemini 3 wants each signed tool call back with its signature."""

    async def test_the_signature_goes_back_with_the_conversation(self):
        """[HP] Two calls in one answer return in one message, the first signed.

        WHY: without the signature, the second call of every diagnosis was a
        400. With the calls in two messages, as datapizza writes them, Gemini
        refused the second as an unsigned turn: a 400 again, tried live
        (docs/decisioni.md, "Secondo fornitore").
        """
        handler, requests = answers(
            completion(
                "tool_calls",
                tool_calls=[
                    tool_call("read_plant", "{}", "call_1", signature="sig-1"),
                    tool_call("read_events", "{}", "call_2"),
                ],
            ),
            completion(
                "tool_calls", tool_calls=[tool_call("submit_diagnosis", SUBMIT, "c3")]
            ),
        )

        run = await diagnose(handler)

        assert run.outcome is Outcome.DIAGNOSED
        [asked] = [m for m in requests[1]["messages"] if m.get("tool_calls")]
        first, second = asked["tool_calls"]
        assert first["extra_content"] == {"google": {"thought_signature": "sig-1"}}
        assert "extra_content" not in second

    async def test_only_the_latest_signatures_are_kept(self, monkeypatch):
        """[EC] One client serves the app for its whole life: the store is bounded."""
        monkeypatch.setattr(adapter, "SIGNATURES_KEPT", 1)
        handler, _ = answers(
            completion(
                "tool_calls", tool_calls=[tool_call("read_plant", "{}", "a", "s1")]
            ),
            completion(
                "tool_calls", tool_calls=[tool_call("read_plant", "{}", "b", "s2")]
            ),
        )
        client = answering(handler)

        for _ in range(2):
            await client.a_invoke("ciao", tools=TOOLS, max_tokens=10)

        assert dict(client._signatures) == {"b": "s2"}


class TestTheKey:
    """The key goes to the SDK, and from there only into the HTTP header."""

    async def test_not_in_the_run_nor_in_what_the_model_reads(self):
        """[SEC] The trace of the diagnosis and every request body leave it out."""
        handler, requests = answers(
            completion("tool_calls", tool_calls=[tool_call("read_plant", "{}", "c1")]),
            completion(
                "tool_calls", tool_calls=[tool_call("submit_diagnosis", SUBMIT, "c2")]
            ),
        )

        run = await diagnose(handler)

        assert run.outcome is Outcome.DIAGNOSED
        assert KEY not in run.model_dump_json()
        assert KEY not in json.dumps(requests)

    async def test_not_in_the_error_nor_in_the_logs(self, caplog, monkeypatch):
        """[SEC] Even from an API that echoes it in its error.

        The module logger is replaced: it is cached on first use, so
        capture_logs cannot see it. caplog takes the logs of datapizza.
        """
        logger = MagicMock()
        monkeypatch.setattr(plant_agent, "logger", logger)
        caplog.set_level("DEBUG")

        with pytest.raises(ExternalServiceError) as exc_info:
            await diagnose(status(401, f"API key {KEY} not valid"))

        assert KEY not in exc_info.value.message
        assert KEY not in str(exc_info.value.details)
        assert KEY not in caplog.text
        assert KEY not in str(logger.mock_calls)
