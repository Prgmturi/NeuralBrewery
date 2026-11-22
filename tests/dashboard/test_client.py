"""Tests for the dashboard's client of the API.

Module under test: src/neuralbrewery/dashboard/client.py
Layer: HTTP client; the real API in memory, or a transport that records

WHY these tests exist: the dashboard is a client of the API and nothing
more. It sends the brewer's token only where the API asks for it, so a
read never carries it; it turns every error of the API, and its silence,
into words for the brewer; and it waits for a diagnosis as long as a
diagnosis takes, up to twelve calls of the model.
"""

import json

import httpx
import pytest

from neuralbrewery.dashboard.client import (
    DIAGNOSIS_TIMEOUT_S,
    TOKEN_HEADER,
    Api,
    ApiError,
    connect,
)
from neuralbrewery.dashboard.settings import DashboardSettings
from tests.dashboard.conftest import TOKEN

# The client passes a timeout, as it must to a real server: the TestClient
# standing in for one ignores it, and says so on every request
pytestmark = pytest.mark.filterwarnings("ignore:You should not use the 'timeout'")


class Recorder:
    """A transport that answers 200 to everything, and keeps each request."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        body = [] if request.url.path == "/approvals" else {}
        return httpx.Response(200, json=body)


def recorded(token: str = TOKEN) -> tuple[Api, Recorder]:
    recorder = Recorder()
    http = httpx.Client(
        transport=httpx.MockTransport(recorder), base_url="http://localhost:8000"
    )
    return Api(http, token), recorder


def failing(error: Exception) -> Api:
    def fail(request: httpx.Request) -> httpx.Response:
        raise error

    http = httpx.Client(
        transport=httpx.MockTransport(fail), base_url="http://localhost:8000"
    )
    return Api(http, TOKEN)


class TestToken:
    def test_a_read_never_carries_the_token(self):
        """[SEC] Plant, queue, diagnosis, simulation: no X-Approval-Token."""
        api, recorder = recorded()

        api.plant()
        api.proposals()
        api.simulation_on()
        api.diagnose()
        api.advance(60)
        api.inject_fault("probe_broken", "TT1", None)
        api.clear_faults()
        api.restart()

        assert len(recorder.requests) == 8
        assert [r for r in recorder.requests if TOKEN_HEADER in r.headers] == []

    def test_proposing_and_deciding_carry_it(self):
        """[SEC] The three routes that ask for it, and only those."""
        api, recorder = recorded()

        api.propose("start_program", "", "Salvatore")
        api.approve("some-id", "Salvatore")
        api.reject("some-id", "Salvatore", "prima controllo TT1")

        assert [r.headers[TOKEN_HEADER] for r in recorder.requests] == [TOKEN] * 3

    def test_with_no_token_it_sends_none_and_shows_the_401(self, http, api):
        """[SEC] The API says no, and the brewer reads it: nothing hidden."""
        proposal = api.propose("start_program", "", "Salvatore")

        with pytest.raises(ApiError) as error:
            Api(http, "").approve(proposal["id"], "Salvatore")

        assert "Token di approvazione mancante o sbagliato" in str(error.value)
        assert "(HTTP 401)" in str(error.value)

    @pytest.mark.parametrize("token", ["wrong-token"])
    def test_with_the_wrong_token_nothing_is_proposed(self, api, log):
        """[SEC] 401 from the API, and nothing written."""
        with pytest.raises(ApiError, match=r"\(HTTP 401\)"):
            api.propose("start_program", "", "Salvatore")

        assert log.events == []


class TestErrorsInWords:
    def test_a_proposal_already_decided_is_409(self, api):
        """[EC] Two approvals of the same proposal: the second is a conflict."""
        proposal = api.propose("start_program", "", "Salvatore")
        api.approve(proposal["id"], "Salvatore")

        with pytest.raises(ApiError) as error:
            api.approve(proposal["id"], "Salvatore")

        assert "non è più in attesa" in str(error.value)
        assert "(HTTP 409)" in str(error.value)

    @pytest.mark.parametrize("agent", [None])
    def test_an_agent_without_a_key_is_503(self, api):
        """[EC] The app without the key of its provider: the brewer learns why."""
        with pytest.raises(ApiError) as error:
            api.diagnose()

        assert "chiave" in str(error.value)
        assert "(HTTP 503)" in str(error.value)

    def test_an_empty_name_is_422(self, api):
        """[EC] The audit needs a name: the API refuses, the brewer reads it."""
        with pytest.raises(ApiError, match=r"Richiesta non valida \(HTTP 422\)"):
            api.propose("start_program", "", "")

    def test_an_api_out_of_reach_is_named(self):
        """[EC] Connection refused: where the dashboard looked, not a traceback."""
        api = failing(httpx.ConnectError("connection refused"))

        with pytest.raises(ApiError) as error:
            api.plant()

        assert "L'API non risponde a http://localhost:8000" in str(error.value)

    def test_an_api_too_slow_is_said(self):
        """[EC] A timeout is a sentence too."""
        api = failing(httpx.ReadTimeout("too slow"))

        with pytest.raises(ApiError, match="non ha risposto in tempo"):
            api.diagnose()

    def test_an_answer_that_is_no_problem_document(self):
        """[EC] A 502 with no JSON body: the status still reaches the brewer."""

        def proxy(request: httpx.Request) -> httpx.Response:
            return httpx.Response(502, text="<html>Bad Gateway</html>")

        http = httpx.Client(transport=httpx.MockTransport(proxy), base_url="http://x")

        with pytest.raises(ApiError) as error:
            Api(http, TOKEN).plant()

        assert str(error.value) == (
            "Il fornitore del modello ha dato una risposta inutilizzabile (HTTP 502)"
        )

    def test_a_status_with_no_sentence_of_its_own(self):
        """[EC] Any other error: the status and the API's detail."""

        def teapot(request: httpx.Request) -> httpx.Response:
            return httpx.Response(418, json={"detail": "short and stout"})

        http = httpx.Client(transport=httpx.MockTransport(teapot), base_url="http://x")

        with pytest.raises(ApiError) as error:
            Api(http, TOKEN).plant()

        assert str(error.value) == "Errore dell'API (HTTP 418): short and stout"


class TestDiagnosis:
    def test_waits_as_long_as_a_diagnosis_takes(self):
        """[EC] Up to twelve calls of the model: httpx's 5 s would cut it."""
        api, recorder = recorded()

        api.plant()
        api.diagnose()

        plant, diagnosis = (r.extensions["timeout"]["read"] for r in recorder.requests)
        assert diagnosis == DIAGNOSIS_TIMEOUT_S >= 120
        assert plant < diagnosis

    def test_the_proposal_of_the_diagnosis_is_in_the_queue(self, api, agent):
        """[HP] The run, and the receipt of its proposal, as the API gives them."""
        answer = api.diagnose()

        assert answer["run"]["diagnosis"]["component"] == "TT1"
        assert answer["queued"]["status"] == "proposed"
        [proposal] = api.proposals()
        assert proposal["id"] == answer["queued"]["proposal_id"]
        assert proposal["events"][0]["actor"] == "agent"
        assert agent.calls == 1


class TestSimulation:
    def test_on_when_the_api_lists_its_routes(self, api):
        """[HP] The API of the compose stack: development, simulation on."""
        assert api.simulation_on() is True

    @pytest.mark.parametrize("simulation", [False])
    def test_off_when_the_api_does_not(self, api):
        """[SEC] PLANT_SIMULATION_CONTROL off: its routes are absent."""
        assert api.simulation_on() is False

    def test_off_when_the_api_describes_nothing(self):
        """[SEC] Out of development there is no /openapi.json, and no simulation."""

        def production(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"detail": "Not Found"})

        http = httpx.Client(
            transport=httpx.MockTransport(production), base_url="http://x"
        )

        assert Api(http, TOKEN).simulation_on() is False

    def test_moves_time_and_breaks_the_plant_through_the_api(self, api):
        """[HP] The fault and the time reach the plant of the app."""
        api.inject_fault("probe_broken", "TT1", None)
        moved = api.advance(60)

        assert moved["sim_time_s"] == 60
        assert api.plant()["readings"]["TT1"]["quality"] == "bad"
        api.clear_faults()
        api.advance(60)
        assert api.plant()["readings"]["TT1"]["quality"] == "good"

    def test_restarts_the_plant_of_the_app(self, api):
        """[HP] Riparti da zero: the plant of the app back at time 0."""
        api.advance(600)

        api.restart()

        assert api.plant()["sim_time_s"] == 0


class TestConnect:
    def test_the_api_of_this_machine_and_no_token_by_default(self):
        """[HP] Without settings: localhost:8000, and nobody approves."""
        settings = DashboardSettings()

        assert settings.api_url == "http://localhost:8000"
        assert settings.approval_token.get_secret_value() == ""

    def test_address_and_token_come_from_the_settings(self, monkeypatch):
        """[HP] DASHBOARD_API_URL and DASHBOARD_APPROVAL_TOKEN, as compose sets them."""
        monkeypatch.setenv("DASHBOARD_API_URL", "http://api:8000")
        monkeypatch.setenv("DASHBOARD_APPROVAL_TOKEN", "from-the-environment")
        recorder = Recorder()

        api = connect(transport=httpx.MockTransport(recorder))
        api.approve("some-id", "Salvatore")

        [request] = recorder.requests
        assert str(request.url) == "http://api:8000/approvals/some-id/approve"
        assert request.headers[TOKEN_HEADER] == "from-the-environment"
        assert json.loads(request.content) == {"by": "Salvatore"}

    def test_the_token_is_never_shown_by_the_settings(self, monkeypatch):
        """[SEC] Printed or logged, the settings hide the token."""
        monkeypatch.setenv("DASHBOARD_APPROVAL_TOKEN", "from-the-environment")

        settings = DashboardSettings()

        assert "from-the-environment" not in repr(settings)
        assert "from-the-environment" not in str(settings.model_dump())
