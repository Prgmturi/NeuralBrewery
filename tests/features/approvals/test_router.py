"""Tests for the routes of the brewer: the queue, propose, approve and reject.

Module under test: src/neuralbrewery/features/approvals/api/
Layer: FastAPI routes; the log in memory, the plant and the executor real

WHY these tests exist: approving is the one step between a proposal and
the plant, and only whoever has APPROVAL_TOKEN takes it. Without the
right token nothing is written and nothing is pressed; the name the
brewer declares is written; the token never comes back, in a response
or in a log. The brewer proposes with the same token, as from user, so
the audit tells the brewer's proposals from those of MCP clients.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from structlog.testing import capture_logs

from neuralbrewery.core.approvals.schemas import Actor
from neuralbrewery.core.config import ServerSettings, Settings
from neuralbrewery.features.approvals.api.dependencies import get_proposal_log
from neuralbrewery.features.approvals.domain.service import ApprovalQueue
from neuralbrewery.features.approvals.persistence.repository import SqlProposalLog
from neuralbrewery.main import create_app
from tests.features.approvals.conftest import BREWER, TOKEN
from tests.features.approvals.fakes import FixedClock
from tests.test_exception_handlers import assert_problem

UNKNOWN = "00000000-0000-4000-8000-000000000000"


async def propose(log, command="set_temperature", arguments=None):
    """A proposal of an MCP client, straight into the log of the app."""
    return await ApprovalQueue(log, FixedClock()).propose(
        command,
        {"vessel": "HLT", "celsius": 70.0} if arguments is None else arguments,
        Actor.MCP,
        "claude-code",
        "acqua per l'impasto",
    )


async def setpoint_of_hlt(client) -> float | None:
    plant = (await client.get("/plant")).json()
    return plant["regulation"]["HLT"]["setpoint_c"]


def test_the_routes_keep_the_log_in_the_table(mock_db_provider):
    """[HP] Outside these tests the log is Postgres, on the app's sessions."""
    assert isinstance(get_proposal_log(mock_db_provider), SqlProposalLog)


class TestQueue:
    async def test_lists_the_newest_first(self, client, log):
        """[HP] No token needed to read: the last proposal at the top."""
        first = await propose(log)
        second = await propose(log, "reset", {})

        response = await client.get("/approvals")

        assert response.status_code == 200
        assert [p["id"] for p in response.json()] == [str(second.id), str(first.id)]

    async def test_one_proposal_with_its_story(self, client, log):
        """[HP] The action, why, the status and every event."""
        proposal = await propose(log)

        body = (await client.get(f"/approvals/{proposal.id}")).json()

        assert body["status"] == "proposed"
        assert body["action"] == {
            "command": "set_temperature",
            "arguments": {"vessel": "HLT", "celsius": 70.0},
        }
        assert body["why"] == "acqua per l'impasto"
        assert body["blocked_reason"] == ""
        [event] = body["events"]
        assert (event["kind"], event["actor"], event["by"]) == (
            "proposed",
            "mcp",
            "claude-code",
        )
        assert event["sim_time_s"] == 0.0

    async def test_a_blocked_proposal_shows_why(self, client, log):
        """[HP] The guardrail's reason is part of the record."""
        proposal = await propose(log, arguments={"vessel": "HLT", "celsius": 99.0})

        body = (await client.get(f"/approvals/{proposal.id}")).json()

        assert body["status"] == "blocked"
        assert "85" in body["blocked_reason"]

    async def test_an_unknown_proposal_is_404(self, client):
        """[EC] 404 in the problem format."""
        assert_problem(await client.get(f"/approvals/{UNKNOWN}"), 404)


class TestApprove:
    async def test_executes_on_the_plant(self, client, log):
        """[HP] Approved with the token: pressed, answered, and the plant changed."""
        proposal = await propose(log)

        response = await client.post(
            f"/approvals/{proposal.id}/approve",
            json={"by": "Salvatore"},
            headers=BREWER,
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "executed"
        approved, executed = body["events"][1:]
        assert (approved["actor"], approved["by"]) == ("user", "Salvatore")
        assert executed["data"] == {"accepted": True, "code": "ok", "reason": ""}
        assert await setpoint_of_hlt(client) == 70.0

    async def test_a_refusal_of_the_controller_is_an_answer(self, client, log):
        """[HP] The kettle is empty: executed, refused, with the reason."""
        proposal = await propose(
            log, "activate_route", {"route": "boil_to_ferm", "liters": 5}
        )

        response = await client.post(
            f"/approvals/{proposal.id}/approve",
            json={"by": "Salvatore"},
            headers=BREWER,
        )

        assert response.status_code == 200
        outcome = response.json()["events"][-1]["data"]
        assert (outcome["accepted"], outcome["code"]) == (False, "source_low")

    async def test_a_second_approval_is_409(self, client, log):
        """[SEC] Pressed once: the second approval is a conflict."""
        proposal = await propose(log)
        url = f"/approvals/{proposal.id}/approve"
        await client.post(url, json={"by": "Salvatore"}, headers=BREWER)

        response = await client.post(url, json={"by": "Salvatore"}, headers=BREWER)

        assert_problem(response, 409)
        assert len(log.events) == 3

    async def test_an_unknown_proposal_is_404(self, client):
        """[EC] With the token, an id that does not exist: 404."""
        response = await client.post(
            f"/approvals/{UNKNOWN}/approve", json={"by": "Salvatore"}, headers=BREWER
        )

        assert_problem(response, 404)

    @pytest.mark.parametrize("body", [{}, {"by": ""}, {"by": "x" * 101}])
    async def test_the_brewer_says_who_they_are(self, client, log, body):
        """[EC] No name, or one too long for the audit: 422."""
        proposal = await propose(log)

        response = await client.post(
            f"/approvals/{proposal.id}/approve", json=body, headers=BREWER
        )

        assert_problem(response, 422)


class TestReject:
    async def test_records_who_and_why_and_presses_nothing(self, client, log):
        """[HP] Rejected with the token; approving it later is 409."""
        proposal = await propose(log)

        response = await client.post(
            f"/approvals/{proposal.id}/reject",
            json={"by": "Salvatore", "reason": "prima controllo TT1"},
            headers=BREWER,
        )
        late = await client.post(
            f"/approvals/{proposal.id}/approve",
            json={"by": "Salvatore"},
            headers=BREWER,
        )

        assert response.status_code == 200
        rejected = response.json()["events"][-1]
        assert (rejected["kind"], rejected["by"]) == ("rejected", "Salvatore")
        assert rejected["data"] == {"reason": "prima controllo TT1"}
        assert_problem(late, 409)
        assert await setpoint_of_hlt(client) is None


class TestPropose:
    """The brewer proposes a button too, from the dashboard (docs/decisioni.md)."""

    async def test_the_brewer_proposes_as_user(self, client, log):
        """[HP] With the token: in the queue as from user, with the declared name."""
        response = await client.post(
            "/approvals",
            json={"command": "resume_program", "why": "TT1 a posto", "by": "Salvatore"},
            headers=BREWER,
        )

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "proposed"
        assert body["action"] == {"command": "resume_program", "arguments": {}}
        assert body["why"] == "TT1 a posto"
        [event] = body["events"]
        assert (event["actor"], event["by"]) == ("user", "Salvatore")
        listed = (await client.get("/approvals")).json()
        assert [p["id"] for p in listed] == [body["id"]]

    async def test_it_waits_for_an_approval_like_any_other(self, client):
        """[HP] Proposing presses nothing: the program starts once approved."""
        proposal = (
            await client.post(
                "/approvals",
                json={"command": "start_program", "by": "Salvatore"},
                headers=BREWER,
            )
        ).json()
        before = (await client.get("/plant")).json()["program"]["status"]

        response = await client.post(
            f"/approvals/{proposal['id']}/approve",
            json={"by": "Salvatore"},
            headers=BREWER,
        )

        assert before == "idle"
        assert response.json()["events"][-1]["data"]["accepted"] is True
        assert (await client.get("/plant")).json()["program"]["status"] == "running"

    async def test_out_of_limits_it_is_blocked_with_the_reason(self, client, log):
        """[SEC] The same guardrail as the agent and MCP: written, never queued."""
        response = await client.post(
            "/approvals",
            json={
                "command": "set_temperature",
                "arguments": {"vessel": "HLT", "celsius": 99.0},
                "by": "Salvatore",
            },
            headers=BREWER,
        )

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "blocked"
        assert "85" in body["blocked_reason"]
        assert [e.kind.value for e in log.events] == ["blocked"]

    @pytest.mark.parametrize(
        "headers",
        [{}, {"X-Approval-Token": "wrong"}],
        ids=["missing", "wrong"],
    )
    async def test_without_the_right_token_401_and_nothing_written(
        self, client, log, headers
    ):
        """[SEC] Whoever proposes as user holds the brewer's token."""
        response = await client.post(
            "/approvals",
            json={"command": "start_program", "by": "Salvatore"},
            headers=headers,
        )

        assert_problem(response, 401)
        assert log.events == []

    @pytest.mark.parametrize(
        "body",
        [{"command": "start_program"}, {"command": "start_program", "by": ""}, {}],
        ids=["no-name", "empty-name", "nothing"],
    )
    async def test_a_command_and_a_name_are_needed(self, client, log, body):
        """[EC] 422, nothing written."""
        response = await client.post("/approvals", json=body, headers=BREWER)

        assert_problem(response, 422)
        assert log.events == []


class TestToken:
    """Only whoever has APPROVAL_TOKEN decides (docs/decisioni.md)."""

    @pytest.mark.parametrize("decision", ["approve", "reject"])
    @pytest.mark.parametrize(
        "headers",
        [{}, {"X-Approval-Token": "wrong"}, {"X-Approval-Token": ""}],
        ids=["missing", "wrong", "empty"],
    )
    async def test_without_the_right_token_401_and_nothing_happens(
        self, client, log, decision, headers
    ):
        """[SEC] 401, nothing written, nothing pressed."""
        proposal = await propose(log)

        response = await client.post(
            f"/approvals/{proposal.id}/{decision}",
            json={"by": "Salvatore"},
            headers=headers,
        )

        assert_problem(response, 401)
        assert "X-Approval-Token" in response.headers["WWW-Authenticate"]
        assert len(log.events) == 1
        assert await setpoint_of_hlt(client) is None

    async def test_401_comes_before_404(self, client):
        """[SEC] Without the token nobody learns which ids exist."""
        response = await client.post(
            f"/approvals/{UNKNOWN}/approve", json={"by": "Salvatore"}
        )

        assert_problem(response, 401)

    async def test_with_no_token_configured_nobody_approves(self, log):
        """[SEC] APPROVAL_TOKEN empty: an empty header does not match it."""
        app = create_app(Settings(server=ServerSettings(trusted_hosts=["testserver"])))
        app.dependency_overrides[get_proposal_log] = lambda: log
        proposal = await propose(log)

        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.post(
                f"/approvals/{proposal.id}/approve",
                json={"by": "Salvatore"},
                headers={"X-Approval-Token": ""},
            )

        assert_problem(response, 401)
        assert len(log.events) == 1

    async def test_a_token_out_of_ascii_is_a_401(self, client, log):
        """[EC] Not a 500: the comparison takes any header."""
        proposal = await propose(log)

        response = await client.post(
            f"/approvals/{proposal.id}/approve",
            json={"by": "Salvatore"},
            headers={"X-Approval-Token": "caffè".encode()},
        )

        assert_problem(response, 401)

    async def test_the_token_never_comes_back(self, client, log):
        """[SEC] Not in the response, its headers, or any line of the log."""
        proposal = await propose(log)

        with capture_logs() as logs:
            response = await client.post(
                f"/approvals/{proposal.id}/approve",
                json={"by": "Salvatore"},
                headers=BREWER,
            )
            proposed = await client.post(
                "/approvals",
                json={"command": "reset", "by": "Salvatore"},
                headers=BREWER,
            )
            listed = await client.get("/approvals")

        assert (response.status_code, proposed.status_code) == (200, 201)
        for answer in (response, proposed, listed):
            assert TOKEN not in answer.text
            assert TOKEN not in str(answer.headers)
        assert logs
        assert TOKEN not in str(logs)
