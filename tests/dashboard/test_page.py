"""Tests for the brewer's dashboard, the page the demo runs from.

Module under test: src/neuralbrewery/dashboard/app.py
Layer: Streamlit page, run by streamlit.testing over the real API in memory

WHY these tests exist: the demo of the speech runs from this page alone.
It must show the plant and its alarms; offer the commands of the
simulation only when the API exposes them; keep a diagnosis on screen
without calling the agent again, which costs money and queues a second
proposal; and let the brewer propose, approve and reject, telling them in
words what the API answered. Approving stays code of the API: without the
right token the page shows the 401, and the token never shows.
"""

import ast
import logging
import runpy
from pathlib import Path

import httpx
import pytest
from streamlit.testing.v1 import AppTest
from structlog.testing import capture_logs

import neuralbrewery.dashboard as dashboard
from neuralbrewery.core.exceptions import ServiceUnavailableError
from neuralbrewery.core.plant.panel import BUTTONS
from neuralbrewery.core.plant.schemas import Command, FaultKind, Proposal, Vessel
from neuralbrewery.dashboard import client as dashboard_client
from neuralbrewery.dashboard.client import Api
from neuralbrewery.dashboard.labels import FAULT_KINDS, PROPOSABLE
from neuralbrewery.features.agents.diagnosis import DiagnosisRun, Outcome
from neuralbrewery.features.approvals.api.dependencies import (
    get_executor,
    get_proposal_log,
)
from tests.dashboard.conftest import (
    CHECK,
    EXPLANATION,
    PAGE,
    RUN,
    TOKEN,
    FakeAgent,
    text_of,
)
from tests.features.approvals.fakes import FakePanel

# The client passes a timeout, as it must to a real server: the TestClient
# standing in for one ignores it, and says so on every request
pytestmark = pytest.mark.filterwarnings("ignore:You should not use the 'timeout'")


def sign(page, name="Salvatore"):
    """The brewer writes their name, as the audit records it."""
    return page.text_input(key="brewer").input(name).run()


def proposal_ids(page):
    return [
        b.key.removeprefix("approve-")
        for b in page.button
        if b.key.startswith("approve-")
    ]


def errors(page):
    return [e.value for e in page.error]


def program(page):
    return {m.label: m.value for m in page.metric}["Programma"]


def propose(page, command, why=""):
    """The brewer proposes a button from the sidebar."""
    page.selectbox(key="propose_command").select(command).run()
    page.text_input(key="propose_why").input(why).run()
    return page.button(key="propose").click().run()


def approve_the_newest(page):
    return page.button(key=f"approve-{proposal_ids(page)[0]}").click().run()


def advance(page, seconds):
    page.number_input(key="advance_s").set_value(seconds).run()
    return page.button(key="advance").click().run()


def break_plant(page, kind, target):
    page.selectbox(key="fault_kind").select(kind).run()
    page.text_input(key="fault_target").input(target).run()
    return page.button(key="inject").click().run()


class BrokenLog:
    """The queue's database, down."""

    async def page(self, limit, offset, actor=None):
        raise ServiceUnavailableError("database")


class TestPlant:
    def test_shows_the_time_the_program_and_no_alarm(self, page):
        """[HP] A brew day not started yet: time zero, program off, all quiet."""
        metrics = {m.label: m.value for m in page.metric}

        assert metrics["Tempo simulato"] == "0:00:00"
        assert metrics["Programma"] == "fermo"
        assert "Nessun allarme" in [s.value for s in page.success]
        assert "TT1" in page.dataframe[0].value["Sigla"].tolist()
        assert not page.exception

    def test_a_broken_probe_shows_as_an_alarm(self, page):
        """[HP] Through the page's own commands: break TT1, move on, read it."""
        page.selectbox(key="fault_kind").select("probe_broken").run()
        page.text_input(key="fault_target").input("TT1").run()
        page.button(key="inject").click().run()
        page.number_input(key="advance_s").set_value(60).run()
        page.button(key="advance").click().run()

        assert any("TT1" in error for error in errors(page))
        assert {m.label: m.value for m in page.metric}["Tempo simulato"] == "0:01:00"


class TestSimulation:
    def test_the_commands_reach_the_plant(self, page):
        """[HP] Inject, move on, clear: each says what it did."""
        page.selectbox(key="fault_kind").select("drive_fault").run()
        page.text_input(key="fault_target").input("M1").run()
        page.number_input(key="fault_value").set_value(11).run()
        page.button(key="inject").click().run()
        assert "drive_fault su M1" in page.success[0].value

        page.button(key="clear").click().run()
        assert "tolti" in page.success[0].value

        page.number_input(key="advance_s").set_value(600).run()
        page.button(key="advance").click().run()
        assert {m.label: m.value for m in page.metric}["Tempo simulato"] == "0:10:00"

    def test_the_watcher_judges_after_each_advance(self, page):
        """[HP] TT5a off by 2 °C: no alarm of the controller, a judgement."""
        break_plant(page, "probe_offset", "TT5a")
        page.number_input(key="fault_value").set_value(2.0).run()
        page.button(key="inject").click().run()

        advance(page, 1200)

        [judgement] = [w.value for w in page.warning]
        assert judgement.startswith("Sorvegliante · **FERM**")
        assert "TT5a" in judgement

    def test_a_fault_the_target_cannot_have_is_said(self, page):
        """[EC] 422 from the API: in words, and nothing breaks."""
        page.selectbox(key="fault_kind").select("probe_broken").run()
        page.text_input(key="fault_target").input("M1").run()
        page.button(key="inject").click().run()

        assert any("(HTTP 422)" in error for error in errors(page))
        assert not page.exception

    @pytest.mark.parametrize("simulation", [False])
    def test_off_the_page_has_no_commands_and_still_works(self, page):
        """[SEC] Simulation off: no command; plant, diagnosis and queue still there."""
        keys = {
            w.key
            for kind in ("button", "number_input", "selectbox")
            for w in getattr(page, kind)
        }

        assert {"advance", "inject", "clear", "fault_kind", "advance_s"} & keys == set()
        assert {"diagnose", "propose"} <= keys
        assert {m.label for m in page.metric} >= {"Tempo simulato", "Programma"}
        assert not page.exception


class TestDiagnosis:
    def test_shows_the_explanation_the_checks_and_the_proposal(self, page, agent):
        """[HP] What the agent says, what to check by hand, what it queued."""
        page.button(key="diagnose").click().run()
        text = text_of(page)

        assert EXPLANATION in text
        assert CHECK in text
        assert "reset" in text
        assert "In coda, in attesa della tua decisione" in text
        assert "read_decisions" in text  # the steps: it read its memory
        assert "1200" in text  # tokens, for the cost
        assert len(proposal_ids(page)) == 1
        assert agent.calls == 1

    def test_stays_on_screen_without_calling_the_agent_again(self, page, agent, log):
        """[SEC] Typing reruns the page: no second diagnosis, no second proposal."""
        page.button(key="diagnose").click().run()

        sign(page)
        [proposal_id] = proposal_ids(page)
        page.text_input(key=f"reason-{proposal_id}").input("prima controllo").run()

        assert agent.calls == 1
        assert len(log.events) == 1
        assert EXPLANATION in text_of(page)

    @pytest.mark.parametrize("agent", [None])
    def test_without_a_key_the_503_is_said(self, page):
        """[EC] The agent cannot run: the brewer reads why, the page goes on."""
        page.button(key="diagnose").click().run()

        assert any("(HTTP 503)" in e and "chiave" in e for e in errors(page))
        assert not page.exception

    @pytest.mark.parametrize(
        "agent",
        [
            FakeAgent(
                DiagnosisRun(
                    outcome=Outcome.REFUSED,
                    diagnosis=None,
                    detail="rifiutata dai filtri",
                    steps=(),
                )
            )
        ],
    )
    def test_a_run_with_no_diagnosis_says_why(self, page):
        """[EC] No diagnosis handed in: the outcome and its detail."""
        page.button(key="diagnose").click().run()

        assert any("rifiutata dai filtri" in w.value for w in page.warning)

    @pytest.mark.parametrize(
        "agent",
        [
            FakeAgent(
                RUN.model_copy(
                    update={
                        "diagnosis": RUN.diagnosis.model_copy(
                            update={"proposal": None, "confirmed": False}
                        )
                    }
                )
            )
        ],
    )
    def test_checks_first_and_nothing_proposed(self, page, log):
        """[HP] The agent proposes nothing: the page says so, the queue stays empty."""
        page.button(key="diagnose").click().run()

        assert "Nessuna proposta: prima le verifiche" in text_of(page)
        assert log.events == []

    @pytest.mark.parametrize(
        "agent",
        [
            FakeAgent(
                RUN.model_copy(
                    update={
                        "diagnosis": RUN.diagnosis.model_copy(
                            update={
                                "checks": (),
                                "proposal": Proposal(
                                    command=Command.SET_TEMPERATURE,
                                    vessel=Vessel.HLT,
                                    celsius=99.0,
                                ),
                            }
                        )
                    }
                )
            )
        ],
    )
    def test_a_proposal_out_of_limits_is_blocked_before_the_queue(self, page):
        """[SEC] The guardrail stops the agent too, and the page says why."""
        page.button(key="diagnose").click().run()

        assert any("Bloccata dal guardrail" in w.value for w in page.warning)
        assert "Verifiche a mano" not in text_of(page)
        assert proposal_ids(page) == []


class TestQueue:
    def test_the_brewer_proposes_then_approves(self, page):
        """[HP] start_program from the page: queued as user, approved, running."""
        sign(page)
        page.selectbox(key="propose_command").select("start_program").run()
        page.text_input(key="propose_why").input("cotta di riferimento").run()
        page.button(key="propose").click().run()

        text = text_of(page)
        assert "start_program" in text
        assert "user · Salvatore" in text
        [proposal_id] = proposal_ids(page)

        page.button(key=f"approve-{proposal_id}").click().run()

        assert "Eseguita" in page.success[0].value
        assert {m.label: m.value for m in page.metric}["Programma"] == "in corso"
        assert proposal_ids(page) == []

    def test_a_blocked_proposal_says_why(self, page, http):
        """[SEC] Out of limits: blocked by the guardrail, with the reason."""
        sign(page)
        http.post(
            "/approvals",
            json={
                "command": "set_temperature",
                "arguments": {"vessel": "HLT", "celsius": 99},
                "by": "x",
            },
            headers={"X-Approval-Token": TOKEN},
        )

        page.run()

        text = text_of(page)
        assert "bloccata dal guardrail" in text
        assert "85" in text
        assert proposal_ids(page) == []

    def test_reject_with_the_reason(self, page, log):
        """[HP] The reason the brewer writes is the one the audit keeps."""
        page.button(key="diagnose").click().run()
        sign(page)
        [proposal_id] = proposal_ids(page)
        reason = "TT1 ha un contatto intermittente: va sostituita prima di riarmare"

        page.text_input(key=f"reason-{proposal_id}").input(reason).run()
        page.button(key=f"reject-{proposal_id}").click().run()

        rejected = log.events[-1]
        assert (rejected.kind.value, rejected.by, rejected.data["reason"]) == (
            "rejected",
            "Salvatore",
            reason,
        )
        assert "rifiutata" in text_of(page)
        assert reason in text_of(page)

    def test_a_refusal_of_the_controller_is_shown_as_one(self, page):
        """[EC] executed is not success: resume with nothing paused is refused."""
        sign(page)
        page.selectbox(key="propose_command").select("resume_program").run()
        page.button(key="propose").click().run()
        [proposal_id] = proposal_ids(page)

        page.button(key=f"approve-{proposal_id}").click().run()

        [warning] = [w.value for w in page.warning]
        assert "Il controllore ha rifiutato resume_program" in warning
        assert "program_state" in warning
        assert "rifiutata dal controllore" in text_of(page)

    def test_a_plant_that_does_not_answer(self, app, open_page):
        """[EC] execution_failed: the brewer reads that the plant said nothing."""
        app.dependency_overrides[get_executor] = lambda: FakePanel(
            raises=TimeoutError()
        )
        page = sign(open_page())
        propose(page, "reset")

        approve_the_newest(page)

        assert any("L'impianto non ha risposto a reset" in e for e in errors(page))
        assert "esecuzione fallita" in text_of(page)

    def test_a_proposal_the_guardrail_blocks_is_said(self, page, api, monkeypatch):
        """[EC] No button of the sidebar is blocked today: if one ever is, it shows."""
        monkeypatch.setattr(
            api,
            "propose",
            lambda *args: {"status": "blocked", "blocked_reason": "fuori dai limiti"},
        )
        sign(page)

        propose(page, "reset")

        assert page.warning[0].value == "Bloccata dal guardrail: fuori dai limiti"

    def test_the_queue_out_of_reach_leaves_the_plant(self, app, open_page):
        """[EC] The database is down: the plant is still there, the queue says why."""
        app.dependency_overrides[get_proposal_log] = lambda: BrokenLog()

        page = open_page()

        assert any("(HTTP 503)" in e for e in errors(page))
        assert program(page) == "fermo"
        assert not page.exception

    def test_a_proposal_decided_meanwhile_is_409_in_words(self, page, api):
        """[EC] Decided in another tab: the click says so, nothing is pressed twice."""
        page.button(key="diagnose").click().run()
        sign(page)
        [proposal_id] = proposal_ids(page)
        api.reject(proposal_id, "Salvatore", "da un'altra scheda")

        page.button(key=f"approve-{proposal_id}").click().run()

        assert any(
            "non è più in attesa" in e and "(HTTP 409)" in e for e in errors(page)
        )

    def test_without_a_name_nothing_is_decided(self, page, log):
        """[EC] The audit needs a name: the page asks for it first."""
        page.button(key="diagnose").click().run()
        [proposal_id] = proposal_ids(page)

        shown = []
        page.button(key=f"approve-{proposal_id}").click().run()
        shown += errors(page)
        page.button(key=f"reject-{proposal_id}").click().run()
        shown += errors(page)
        propose(page, "start_program")
        shown += errors(page)

        assert len(shown) == 3
        assert all("Scrivi il tuo nome" in e for e in shown)
        assert len(log.events) == 1


class TestToken:
    @pytest.mark.parametrize("token", ["wrong-token", ""], ids=["wrong", "none"])
    def test_without_the_right_token_approve_and_reject_show_401(
        self, page, http, log, token
    ):
        """[SEC] The API refuses, the page shows it, the proposal still waits."""
        page.button(key="diagnose").click().run()
        sign(page)
        [proposal_id] = proposal_ids(page)

        page.button(key=f"approve-{proposal_id}").click().run()
        approve_errors = errors(page)
        page.button(key=f"reject-{proposal_id}").click().run()

        for shown in (approve_errors, errors(page)):
            assert any(
                "Token di approvazione" in e and "(HTTP 401)" in e for e in shown
            )
        assert [e.kind.value for e in log.events] == ["proposed"]
        assert proposal_ids(page) == [proposal_id]

    def test_the_token_never_shows_nor_is_logged(self, page, caplog):
        """[SEC] Through a whole round: not on the page, not in any log."""
        caplog.set_level(logging.DEBUG)
        seen = []
        with capture_logs() as logs:
            sign(page)
            page.selectbox(key="propose_command").select("start_program").run()
            page.button(key="propose").click().run()
            seen.append(text_of(page))
            page.button(key=f"approve-{proposal_ids(page)[0]}").click().run()
            seen.append(text_of(page))
            page.button(key="diagnose").click().run()
            seen.append(text_of(page))
            page.button(key=f"reject-{proposal_ids(page)[0]}").click().run()
            seen.append(text_of(page))

        assert all(TOKEN not in shown for shown in seen)
        assert TOKEN not in caplog.text
        assert TOKEN not in str(logs)


class TestApiOutOfReach:
    def test_the_page_says_where_it_looked(self, monkeypatch):
        """[EC] The API is off: one sentence, no traceback."""

        def refused(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused")

        http = httpx.Client(
            transport=httpx.MockTransport(refused), base_url="http://localhost:8000"
        )
        monkeypatch.setattr(dashboard_client, "connect", lambda: Api(http, TOKEN))

        page = AppTest.from_file(str(PAGE), default_timeout=30).run()

        assert any(
            "L'API non risponde a http://localhost:8000" in e for e in errors(page)
        )
        assert not page.exception


class TestBoundaries:
    def test_imported_as_a_module_it_draws_nothing_and_calls_no_api(self, monkeypatch):
        """[SEC] tests/core/database imports every module of the app: this one too.

        WHY: the page drew itself on import, and called the API of
        DASHBOARD_API_URL: the stack on this machine, or nothing in CI,
        where the import failed. Found on 15 November.
        """
        calls = []
        monkeypatch.setattr(dashboard_client, "connect", lambda: calls.append(1))

        names = runpy.run_path(str(PAGE), run_name="neuralbrewery.dashboard.app")

        assert calls == []
        assert callable(names["main"])

    def test_the_dashboard_imports_nothing_of_the_app(self):
        """[SEC] A client of the API, like curl: no port, adapter or feature.

        import-linter checks the same in CI; this reads the files themselves.
        """
        folder = Path(dashboard.__file__).parent
        imported = set()
        for path in folder.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    imported.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module)

        of_the_app = {
            name
            for name in imported
            if name.startswith("neuralbrewery")
            and not name.startswith("neuralbrewery.dashboard")
        }
        assert of_the_app == set()
        assert "httpx" in imported

    def test_it_proposes_the_buttons_that_take_no_argument(self):
        """[HP] The names the page offers are the panel's: none drifts."""
        assert set(PROPOSABLE) == {
            command.value
            for command, button in BUTTONS.items()
            if not button.needs and not button.takes
        }

    def test_it_offers_every_fault_of_the_plant(self):
        """[HP] The faults the page offers are those the API takes."""
        assert set(FAULT_KINDS) == {kind.value for kind in FaultKind}


class TestTheRoundOfTheDemo:
    def test_a_broken_probe_from_alarm_to_a_running_program(self, page, agent):
        """[HP] The story of the speech, from the page alone, the agent faked.

        Start the brew; TT1 breaks while the water heats, the program
        pauses; TT1 comes back, the block stays; the agent proposes reset,
        the brewer approves it, then proposes resume_program and approves
        it; the program runs again.
        """
        sign(page)
        propose(page, "start_program", "cotta di riferimento")
        approve_the_newest(page)
        assert program(page) == "in corso"

        advance(page, 600)
        break_plant(page, "probe_broken", "TT1")
        advance(page, 300)
        assert program(page) == "in pausa"
        assert any(c.value.startswith("In pausa: ") for c in page.caption)

        page.button(key="clear").click().run()
        advance(page, 300)
        assert any("(bloccato: serve reset)" in e for e in errors(page))

        page.button(key="diagnose").click().run()
        approve_the_newest(page)
        assert page.success[0].value == "Eseguita: il controllore ha accettato reset."

        propose(page, "resume_program", "TT1 a posto")
        approve_the_newest(page)
        advance(page, 60)

        assert program(page) == "in corso"
        assert errors(page) == []
        assert agent.calls == 1
