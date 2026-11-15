"""Tests for the agent endpoint: diagnose the plant now, queue the proposal.

Module under test: src/neuralbrewery/features/agents/router.py
Layer: FastAPI route; the plant agent on a scripted client, no network

WHY these tests exist: the plant agent proposes like the MCP server, into
the same queue, as from "agent". Served by the API, a failure of its
provider, Claude or the second one, must answer 503 or 502 in the problem
format (ADR 0006), not 500, and the CI must never call the network: the
scripted client of M5 answers here.
"""

from types import SimpleNamespace

import httpx
import pytest
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from neuralbrewery.adapters.claude.client import create_client
from neuralbrewery.adapters.openai_compat.client import SERVICE as COMPAT_SERVICE
from neuralbrewery.adapters.openai_compat.client import OpenAICompatClient
from neuralbrewery.adapters.openai_compat.client import (
    create_client as create_compat_client,
)
from neuralbrewery.core.approvals.protocols import ProposalInbox
from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.config import ServerSettings, Settings
from neuralbrewery.core.config.agent import AgentSettings
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.config.openai_compat import OpenAICompatSettings
from neuralbrewery.core.plant.dependencies import PLANT_READER
from neuralbrewery.features.agents.plant_agent import PlantAgent
from neuralbrewery.features.agents.router import (
    get_plant_agent,
    get_proposal_inbox,
)
from tests.features.agents.fakes import (
    DIAGNOSIS,
    PROPOSAL_ID,
    RecordingInbox,
    ScriptedClient,
    call,
)
from tests.test_exception_handlers import assert_problem

GENERATION = {"max_tokens": 16000}
URL = "/agents/plant/diagnose"


@pytest.fixture
def inbox() -> RecordingInbox:
    return RecordingInbox()


@pytest.fixture
def agent_answers(app, inbox):
    """The app's plant agent, on a client given by the test."""

    def use(client) -> None:
        agent = PlantAgent(PLANT_READER.get(app.state), client, GENERATION)
        app.dependency_overrides[get_plant_agent] = lambda: agent
        app.dependency_overrides[get_proposal_inbox] = lambda: inbox

    return use


class TestDiagnose:
    async def test_the_proposal_of_the_diagnosis_goes_in_the_queue(
        self, client, agent_answers, inbox
    ):
        """[HP] Diagnosed; the proposal reaches the inbox as from the agent."""
        agent_answers(ScriptedClient(call("submit_diagnosis", **DIAGNOSIS)))

        response = await client.post(URL)

        assert response.status_code == 200
        body = response.json()
        assert body["run"]["outcome"] == "diagnosed"
        assert body["run"]["diagnosis"]["component"] == "TT5a"
        assert body["queued"] == {
            "proposal_id": str(PROPOSAL_ID),
            "status": "proposed",
            "reason": "",
        }
        assert inbox.proposals == [
            (
                "set_temperature",
                {"vessel": "FERM", "celsius": 21.0},
                Actor.AGENT,
                "plant_agent",
                DIAGNOSIS["explanation"],
            )
        ]

    async def test_no_command_queues_nothing(self, client, agent_answers, inbox):
        """[HP] The checks come first: a diagnosis, and no proposal."""
        checks_first = {**DIAGNOSIS, "command": None, "confirmed": False}
        agent_answers(ScriptedClient(call("submit_diagnosis", **checks_first)))

        body = (await client.post(URL)).json()

        assert body["run"]["outcome"] == "diagnosed"
        assert body["queued"] is None
        assert inbox.proposals == []


class TestUnavailable:
    async def test_without_a_key_the_agent_is_503(self, client):
        """[EC] ANTHROPIC_API_KEY empty, the default: no agent, 503."""
        body = assert_problem(await client.post(URL), 503)

        assert body["service"] == "Claude"

    async def test_anthropic_out_of_reach_is_503(self, client, agent_answers, inbox):
        """[EC] The real client of the app, its connection refused: 503, problem.

        WHY: ADR 0006. An exception of the SDK reached the exception handlers
        as an unknown error, a 500 with no hint to retry.
        """

        def refused(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("refused")

        claude = create_client(ClaudeSettings(api_key="sk-ant-test"))
        claude.a_client = AsyncAnthropic(
            api_key="sk-ant-test",
            base_url="http://anthropic.test",
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(refused)),
            max_retries=0,
        )
        agent_answers(claude)

        assert_problem(await client.post(URL), 503)
        assert inbox.proposals == []


def second_provider_answering(handler) -> OpenAICompatClient:
    """The second provider's client of the app, its HTTP answered by handler."""
    compat = create_compat_client(OpenAICompatSettings(api_key="gm-test"))
    compat.a_client = AsyncOpenAI(
        api_key="gm-test",
        base_url="http://compat.test/v1/",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        max_retries=0,
    )
    return compat


def refused(request: httpx.Request) -> httpx.Response:
    raise httpx.ConnectError("refused")


def over_the_limits(request: httpx.Request) -> httpx.Response:
    return httpx.Response(429, json=[{"error": {"code": 429, "message": "quota"}}])


def unusable(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "id": "x",
            "object": "chat.completion",
            "created": 0,
            "model": "m",
            "choices": [],
        },
    )


class TestOnTheSecondProvider:
    """AGENT_PROVIDER=openai_compat: the same endpoint, the same answers.

    WHY: the agent does not know its provider, and neither does a client of
    the API: an error is 503 or 502 in the problem format with either.
    """

    @pytest.fixture
    def settings(self) -> Settings:
        """The second provider chosen; only Claude has a key."""
        return Settings(
            server=ServerSettings(trusted_hosts=["testserver"]),
            agent=AgentSettings(provider="openai_compat"),
            claude=ClaudeSettings(api_key="sk-ant-test"),
        )

    async def test_without_its_key_the_agent_is_503(self, client):
        """[EC] The key of Claude is no help: the chosen provider has none."""
        body = assert_problem(await client.post(URL), 503)

        assert body["service"] == COMPAT_SERVICE

    @pytest.mark.parametrize(
        ("handler", "code"),
        [(refused, 503), (over_the_limits, 503), (unusable, 502)],
        ids=["unreachable", "over-the-limits", "unusable"],
    )
    async def test_its_errors_keep_the_problem_format(
        self, client, agent_answers, inbox, handler, code
    ):
        """[EC] The real client of the app: 503 retry later, 502 do not."""
        agent_answers(second_provider_answering(handler))

        assert_problem(await client.post(URL), code)
        assert inbox.proposals == []


def test_the_agent_proposes_through_the_inbox_of_the_app(app):
    """[HP] Outside these tests, the inbox bootstrap.py built: the queue's port."""
    inbox = get_proposal_inbox(SimpleNamespace(app=app))

    assert isinstance(inbox, ProposalInbox)
