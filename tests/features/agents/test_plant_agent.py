"""Tests for the plant agent: its loop, its tools and its verdict.

Module under test: src/neuralbrewery/features/agents/
The model is a scripted client (fakes.py); the plant is the real simulated
one, in process. No network.

WHY these tests exist: the evals call Claude, and they cost money and run
by hand. Everything around the model runs here instead: the alarms the
agent starts from, the tools that read the plant, the diagnosis checked
against what the plant can be told, the outcome of a refusal or of an
answer with no diagnosis, the trace of every step. And rule 1: the agent
reads the plant and can command nothing.
"""

import ast
import json
from pathlib import Path

import pytest

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.plant.protocols import (
    PlantCommander,
    PlantReader,
    SimulationControl,
)
from neuralbrewery.core.plant.schemas import Command, Fault, FaultKind, Route, Vessel
from neuralbrewery.features.agents.diagnosis import FaultType, Outcome
from neuralbrewery.features.agents.plant_agent import PlantAgent
from neuralbrewery.features.agents.tools import (
    Submission,
    reading_tools,
    submit_tool,
)
from tests.features.agents.fakes import (
    DIAGNOSIS,
    USAGE,
    ScriptedClient,
    call,
    refuse,
    say,
    together,
)

ROOT = Path(__file__).parents[3]
GENERATION = {"max_tokens": 16000, "output_config": {"effort": "high"}}


@pytest.fixture
async def plant() -> InProcessPlant:
    """A fermentation where TT5a reads 2 °C high: the watcher has judged it."""
    plant = InProcessPlant(fermentation(progress=0.3))
    await plant.inject_fault(
        Fault(kind=FaultKind.PROBE_OFFSET, target="TT5a", value=2.0)
    )
    await plant.advance(20 * 60)
    return plant


def agent_for(plant: PlantReader, client: ScriptedClient, **kwargs) -> PlantAgent:
    return PlantAgent(plant, client, GENERATION, **kwargs)


class TestDiagnosis:
    async def test_reads_the_plant_then_submits(self, plant):
        """[HP] The happy path of an eval: read, judge, submit."""
        client = ScriptedClient(
            call("read_plant"),
            call("run_watcher"),
            call("submit_diagnosis", **DIAGNOSIS),
        )

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.DIAGNOSED
        diagnosis = run.diagnosis
        assert (diagnosis.component, diagnosis.fault_type) == (
            "TT5a",
            FaultType.MEASUREMENT,
        )
        proposal = diagnosis.proposal
        assert (proposal.command, proposal.vessel, proposal.celsius) == (
            Command.SET_TEMPERATURE,
            Vessel.FERM,
            21.0,
        )
        assert [step.name for step in run.steps if step.kind == "tool"] == [
            "read_plant",
            "run_watcher",
            "submit_diagnosis",
        ]

    async def test_starts_from_the_alarms_of_controller_and_watcher(self, plant):
        """[HP] The diagnosis is started by an alarm, and the agent is told which."""
        client = ScriptedClient(call("submit_diagnosis", **DIAGNOSIS))

        await agent_for(plant, client).diagnose()

        message = client.first_message()
        assert "probes_disagree" in message
        assert "TT5a e TT5b non concordano" in message
        assert "Nessun allarme del controllore" in message

    async def test_the_message_says_where_the_program_stopped_and_why(self):
        """[HP] A brew day: the program, its reason, the facts of the controller."""
        plant = InProcessPlant(brew_day())
        assert (await plant.start_program()).accepted
        await plant.advance(60)
        await plant.inject_fault(Fault(kind=FaultKind.PROBE_BROKEN, target="TT1"))
        await plant.advance(2)
        client = ScriptedClient(call("submit_diagnosis", **DIAGNOSIS))

        await agent_for(plant, client).diagnose()

        message = client.first_message()
        assert "Programma: paused, passo 1 (Scalda l'acqua), motivo:" in message
        assert "signal_fault su TT1, da 0 h 01 min" in message
        assert "control_probe_fault su HLT" in message
        assert "Nessun giudizio del sorvegliante." in message

    async def test_the_tools_give_the_plant_as_the_controller_shows_it(self, plant):
        """[HP] Readings, events, history and judgements, from the real plant."""
        client = ScriptedClient(
            call("read_plant"),
            call("read_events", since_minutes=30),
            call("read_history", tag="TT5a", since_minutes=10),
            call("run_watcher"),
            call("submit_diagnosis", **DIAGNOSIS),
        )

        run = await agent_for(plant, client).diagnose()

        results = {step.name: step.result for step in run.steps if step.kind == "tool"}
        tt5a = (await plant.snapshot()).readings["TT5a"]
        assert f'"value":{tt5a.value}' in results["read_plant"]
        assert "set_temperature" in results["read_events"]  # 19 °C, at the start
        assert results["read_history"].count("[") == 1 + 11  # ten minutes, by minute
        assert "probes_disagree" in results["run_watcher"]

    async def test_an_unknown_tag_is_an_answer_to_the_model(self, plant):
        """[EC] A wrong tag must not end the diagnosis: the model reads again."""
        client = ScriptedClient(
            call("read_history", tag="TT9"),
            call("submit_diagnosis", **DIAGNOSIS),
        )

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.DIAGNOSED
        assert "TT9" in run.steps[1].result


class TestOutcomes:
    async def test_a_text_answer_is_no_diagnosis(self, plant):
        """[EC] The model answers in text: nothing an eval can check."""
        client = ScriptedClient(call("read_plant"), say("Credo sia la sonda TT5a."))

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.NO_DIAGNOSIS
        assert run.diagnosis is None
        assert "Credo sia la sonda TT5a." in run.detail

    @pytest.mark.parametrize("stop_reason", ["refusal", "content_filter"])
    async def test_a_refusal_stops_at_the_first_call(self, plant, stop_reason):
        """[EC] datapizza would ask again until max_steps: the hook stops it.

        Claude and the second provider name a refusal differently.
        """
        client = ScriptedClient(refuse(stop_reason))

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.REFUSED
        assert "Claude" not in run.detail
        assert len(client.calls) == 1

    async def test_the_steps_run_out(self, plant):
        """[EC] A model that only reads is stopped, and says nothing."""
        client = ScriptedClient(call("read_plant"))

        run = await agent_for(plant, client, max_steps=3).diagnose()

        assert run.outcome is Outcome.NO_DIAGNOSIS
        assert len(client.calls) == 3
        assert "3" in run.detail

    @pytest.mark.parametrize(
        ("change", "error"),
        [
            ({"vessel": None}, "vessel"),  # a setpoint for which vessel?
            ({"fault_type": "electrical"}, "fault_type"),
            ({"command": "open_valve"}, "command"),  # not a button of the panel
        ],
    )
    async def test_a_diagnosis_the_plant_could_not_take_is_invalid(
        self, plant, change, error
    ):
        """[EC] Arguments outside the schema end the run, and say what was wrong."""
        client = ScriptedClient(call("submit_diagnosis", **{**DIAGNOSIS, **change}))

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.INVALID_DIAGNOSIS
        assert run.diagnosis is None
        assert error in run.detail

    async def test_two_diagnoses_in_one_turn_the_first_counts(self, plant):
        """[EC] Tools may come in parallel: the second hand-in changes nothing."""
        other = {**DIAGNOSIS, "component": "TT5b"}
        client = ScriptedClient(
            together(
                call("submit_diagnosis", **DIAGNOSIS),
                call("submit_diagnosis", **other),
            )
        )

        run = await agent_for(plant, client).diagnose()

        assert run.diagnosis.component == "TT5a"
        assert run.steps[-1].result == "Diagnosi già consegnata."

    async def test_no_command_is_a_proposal_too(self, plant):
        """[HP] When checks come first, the agent proposes nothing to press."""
        no_command = {**DIAGNOSIS, "command": None, "vessel": None, "celsius": None}
        client = ScriptedClient(call("submit_diagnosis", **no_command))

        run = await agent_for(plant, client).diagnose()

        assert run.outcome is Outcome.DIAGNOSED
        assert run.diagnosis.proposal is None

    async def test_a_route_needs_its_name(self, plant):
        """[EC] Each command takes the arguments of its button, and only those."""
        transfer = {
            **DIAGNOSIS,
            "command": "activate_route",
            "vessel": None,
            "celsius": None,
            "route": "hlt_to_mash",
            "liters": 13.5,
        }
        client = ScriptedClient(call("submit_diagnosis", **transfer))

        run = await agent_for(plant, client).diagnose()

        proposal = run.diagnosis.proposal
        assert (proposal.command, proposal.route, proposal.liters) == (
            Command.ACTIVATE_ROUTE,
            Route.HLT_TO_MASH,
            13.5,
        )


class TestToolSchemas:
    def test_every_schema_is_plain_json(self, plant):
        """[EC] What goes to the API must be written by the JSON encoder as it is.

        WHY: for an optional enum, datapizza's schema held references of
        jsonref, which json.dumps cannot write, and a $defs: the first real
        call would have failed, and no test without network would have seen it.
        """
        tools = [*reading_tools(plant), submit_tool(Submission())]

        for tool in tools:
            text = json.dumps(
                {"properties": tool.properties, "required": tool.required}
            )
            assert "$ref" not in text

        submit = tools[-1]
        assert submit.properties["command"]["anyOf"][0]["enum"] == [
            command.value for command in Command
        ]
        assert submit.required == [
            "component",
            "fault_type",
            "confirmed",
            "explanation",
            "checks",
        ]


class TestCalls:
    async def test_every_call_leaves_the_tool_to_the_model(self, plant):
        """[EC] A forced tool_choice is a 400 on the current Claude models."""
        client = ScriptedClient(
            call("read_plant"), call("submit_diagnosis", **DIAGNOSIS)
        )

        await agent_for(plant, client).diagnose()

        assert [c["tool_choice"] for c in client.calls] == ["auto", "auto"]

    async def test_every_call_carries_the_generation_arguments(self, plant):
        """[HP] Tokens and effort reach the client on every call, not just the first."""
        client = ScriptedClient(
            call("read_plant"), call("submit_diagnosis", **DIAGNOSIS)
        )

        await agent_for(plant, client).diagnose()

        for made in client.calls:
            assert made["max_tokens"] == 16000
            assert made["output_config"] == {"effort": "high"}


class TestTrace:
    async def test_every_step_is_traced_with_its_stop_reason_and_tokens(self, plant):
        """[HP] The audit trail: each call of the model and each tool, in order."""
        client = ScriptedClient(
            call("read_plant"), call("submit_diagnosis", **DIAGNOSIS)
        )

        run = await agent_for(plant, client).diagnose()

        assert [(step.kind, step.name) for step in run.steps] == [
            ("model", "scripted"),
            ("tool", "read_plant"),
            ("model", "scripted"),
            ("tool", "submit_diagnosis"),
        ]
        model_steps = [step for step in run.steps if step.kind == "model"]
        assert [step.stop_reason for step in model_steps] == ["tool_use", "tool_use"]
        assert run.input_tokens == 2 * USAGE["prompt_tokens"]
        assert run.output_tokens == 2 * USAGE["completion_tokens"]
        assert run.cached_tokens == 2 * USAGE["cached_tokens"]
        assert "'component': 'TT5a'" in run.steps[3].arguments  # as datapizza has it


class TestRuleOne:
    """No agent receives PlantCommander (AGENTS.md, rule 1)."""

    def test_the_agent_holds_a_reader_and_nothing_else(self, plant):
        """[SEC] Handed the in-process plant, all three ports at once."""
        agent = agent_for(plant, ScriptedClient(say("")))

        assert isinstance(agent.reader, PlantReader)
        assert not isinstance(agent.reader, PlantCommander)
        assert not isinstance(agent.reader, SimulationControl)

    @pytest.mark.parametrize(
        "path",
        [
            *sorted((ROOT / "src/neuralbrewery/features/agents").glob("*.py")),
            ROOT / "src/neuralbrewery/core/plant/watcher.py",
        ],
        ids=lambda path: path.name,
    )
    def test_no_code_of_the_agent_names_the_command_ports(self, path):
        """[SEC] Not imported, not typed, not referred to: by name."""
        names = {
            node.id if isinstance(node, ast.Name) else node.attr
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
            if isinstance(node, ast.Name | ast.Attribute)
        } | {
            alias.name
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
            if isinstance(node, ast.ImportFrom)
            for alias in node.names
        }

        assert not names & {"PlantCommander", "SimulationControl"}

    def test_a_proposal_names_only_the_buttons_of_the_panel(self):
        """[SEC] Every command the agent may propose is one the executor knows."""
        buttons = {
            name
            for name, member in vars(PlantCommander).items()
            if callable(member) and not name.startswith("_")
        }

        assert {command.value for command in Command} == buttons
