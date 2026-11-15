"""Dashboard fixtures: the real API in memory, and no network at all.

The dashboard talks to the API over HTTP. Here its HTTP client is a
TestClient of the real app, which is an httpx.Client: the 401, the 409,
the 503 and the routes of the simulation come from the app itself, not
from JSON written by hand. The queue is the log in memory of the approvals
tests, the plant the one in the app's process, and the agent a fake with
one fixed diagnosis, since the real one would call a model.
"""

from collections.abc import Callable, Iterator
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

import neuralbrewery.dashboard as dashboard
from neuralbrewery.core.config import ApprovalSettings, ServerSettings, Settings
from neuralbrewery.core.config.plant import PlantSettings
from neuralbrewery.core.plant.dependencies import PLANT_READER
from neuralbrewery.core.plant.schemas import Command, Proposal
from neuralbrewery.dashboard import client as dashboard_client
from neuralbrewery.dashboard.client import Api
from neuralbrewery.dashboard.settings import DashboardSettings
from neuralbrewery.features.agents.diagnosis import (
    Diagnosis,
    DiagnosisRun,
    FaultType,
    Outcome,
    Step,
)
from neuralbrewery.features.agents.router import get_plant_agent, get_proposal_inbox
from neuralbrewery.features.approvals.api.dependencies import get_proposal_log
from neuralbrewery.features.approvals.api.inbox import QueueInbox
from tests.features.approvals.fakes import InMemoryProposalLog

TOKEN = "dashboard-test-token-7f3a"
PAGE = Path(dashboard.__file__).parent / "app.py"

EXPLANATION = "La sonda TT1 era guasta ed è tornata a posto: resta il blocco."
CHECK = "Controlla il cablaggio di TT1 prima di riarmare"
RUN = DiagnosisRun(
    outcome=Outcome.DIAGNOSED,
    diagnosis=Diagnosis(
        component="TT1",
        fault_type=FaultType.MEASUREMENT,
        confirmed=True,
        explanation=EXPLANATION,
        checks=(CHECK,),
        proposal=Proposal(command=Command.RESET),
    ),
    detail="",
    steps=(
        Step(
            kind="model",
            name="claude-sonnet-5-5",
            stop_reason="tool_use",
            input_tokens=1200,
            output_tokens=300,
            cached_tokens=800,
        ),
        Step(kind="tool", name="read_decisions", arguments="{}", result="[]"),
    ),
)


class FakeAgent:
    """The plant agent of the app, without a model: one diagnosis, counted."""

    def __init__(self, run: DiagnosisRun = RUN) -> None:
        self.run = run
        self.calls = 0

    async def diagnose(self) -> DiagnosisRun:
        self.calls += 1
        return self.run


@pytest.fixture(autouse=True)
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Any request that would leave this process fails the test."""

    def refuse(self: httpx.HTTPTransport, request: httpx.Request) -> httpx.Response:
        raise AssertionError(
            f"a test of the dashboard called the network: {request.url}"
        )

    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", refuse)


@pytest.fixture(autouse=True)
def hermetic_dashboard_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Neither the local .env nor exported DASHBOARD_* reach a test.

    hermetic_settings of tests/conftest.py isolates the app's settings only:
    the dashboard's are not part of them.
    """
    monkeypatch.setitem(DashboardSettings.model_config, "env_file", None)
    for field in DashboardSettings.model_fields:
        monkeypatch.delenv(f"DASHBOARD_{field}".upper(), raising=False)


@pytest.fixture
def simulation() -> bool:
    """Whether the API exposes the routes of the simulation."""
    return True


@pytest.fixture
def settings(simulation: bool) -> Settings:
    return Settings(
        server=ServerSettings(trusted_hosts=["testserver"]),
        approvals=ApprovalSettings(token=TOKEN),
        plant=PlantSettings(simulation_control=simulation),
    )


@pytest.fixture
def log() -> InMemoryProposalLog:
    return InMemoryProposalLog()


@pytest.fixture
def agent() -> FakeAgent | None:
    """None: the app as it is without a key, whose agent answers 503."""
    return FakeAgent()


@pytest.fixture
def app(app, log, agent):
    """The app of tests/conftest.py: the queue in memory, the fake agent."""
    app.dependency_overrides[get_proposal_log] = lambda: log
    inbox = QueueInbox(lambda: log, PLANT_READER.get(app.state))
    app.dependency_overrides[get_proposal_inbox] = lambda: inbox
    if agent is not None:
        app.dependency_overrides[get_plant_agent] = lambda: agent
    return app


@pytest.fixture
def http(app) -> Iterator[TestClient]:
    """One event loop for every request, as a server would have."""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def token() -> str:
    """The token the dashboard holds."""
    return TOKEN


@pytest.fixture
def api(http: TestClient, token: str) -> Api:
    return Api(http, token)


@pytest.fixture
def open_page(monkeypatch: pytest.MonkeyPatch, api: Api) -> Callable[[], AppTest]:
    """The page as the brewer opens it, talking to the API above."""
    monkeypatch.setattr(dashboard_client, "connect", lambda: api)

    def run() -> AppTest:
        return AppTest.from_file(str(PAGE), default_timeout=30).run()

    return run


@pytest.fixture
def page(open_page: Callable[[], AppTest]) -> AppTest:
    return open_page()


def text_of(page: AppTest) -> str:
    """Every text the page shows: what a brewer, or a screen recording, sees."""
    kinds = (
        "title", "header", "subheader", "markdown", "caption", "text", "code",
        "json", "error", "warning", "info", "success", "exception", "metric",
        "dataframe", "table", "expander", "button", "text_input", "selectbox",
        "number_input",
    )  # fmt: skip
    parts = []
    for kind in kinds:
        for element in getattr(page, kind):
            for name in ("label", "value", "body"):
                parts.append(str(getattr(element, name, "")))
    return "\n".join(parts)
