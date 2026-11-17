"""The demo through the whole stack: compose up, the plant, the queue.

WHY this test exists: the demo of the speech starts from a clean clone and
docker compose up, with no .env. The unit tests run the app in memory;
here the images, the migrations, Postgres and the dashboard run as the
demo runs them, in CI after docker compose up --wait. It replaces the
login through Keycloak, gone in M10 with the login.

Run it on a stack you can throw away, as CI does: the audit keeps every
proposal, and this test adds one (by "e2e").
"""

import os

import pytest

# The approval token of compose.yaml, public: the development stack only
TOKEN = {"X-Approval-Token": "brewer-dev-token"}


def test_the_api_is_ready(api):
    """[HP] /health/ready: the database answers, with the migrations applied."""
    response = api.get("/health/ready")

    assert response.status_code == 200, response.text
    assert response.json()["checks"] == {"database": {"status": "healthy"}}


def test_the_plant_answers(api):
    """[HP] /plant: the simulated plant lives in the API, at its start."""
    response = api.get("/plant")

    assert response.status_code == 200, response.text


def test_the_dashboard_answers(dashboard):
    """[HP] The page the demo runs from, in its own image."""
    assert dashboard.get("/_stcore/health").text == "ok"
    assert dashboard.get("/").status_code == 200


def test_a_proposal_goes_from_the_queue_to_the_plant(api):
    """[HP] Propose, approve with the token: the executor presses, the audit says so.

    reset, which re-arms only what no longer has its cause: on a plant at
    its start it changes nothing.
    """
    proposed = api.post(
        "/approvals",
        json={"command": "reset", "why": "e2e of the stack", "by": "e2e"},
        headers=TOKEN,
    )
    assert proposed.status_code == 201, proposed.text
    assert proposed.json()["status"] == "proposed"

    approved = api.post(
        f"/approvals/{proposed.json()['id']}/approve",
        json={"by": "e2e"},
        headers=TOKEN,
    )

    assert approved.status_code == 200, approved.text
    assert [event["kind"] for event in approved.json()["events"]] == [
        "proposed",
        "approved",
        "executed",
    ]


def test_approving_needs_the_token(api):
    """[SEC] Without the token nobody proposes: 401, nothing queued."""
    response = api.post("/approvals", json={"command": "reset", "by": "e2e"})

    assert response.status_code == 401, response.text


@pytest.mark.skipif(
    os.environ.get("E2E_NO_AGENT_KEY") != "true",
    reason="with a key the diagnosis calls the model and costs: CI sets it",
)
def test_the_diagnosis_without_a_key_answers_503(api):
    """[EC] No key for the agent: 503, and the rest of the demo still works."""
    response = api.post("/agents/plant/diagnose")

    assert response.status_code == 503, response.text
