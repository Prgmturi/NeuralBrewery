"""The plant in the process of the API: who gets which port.

Modules under test: src/neuralbrewery/bootstrap.py (init_plant) and every
module of src/ that could name the commander
Layer: Composition of the app

WHY these tests exist: the in-process adapter implements the three ports
in one object (AGENTS.md, rule 1). Handed out as it is, any code that
reads it from app.state could command the plant or move its time. Only
the executor may hold PlantCommander, and SimulationControl exists only
when PLANT_SIMULATION_CONTROL is on.
"""

import ast
from pathlib import Path

import pytest

import neuralbrewery
from neuralbrewery.adapters.claude.client import ClaudeClient
from neuralbrewery.adapters.openai_compat.client import OpenAICompatClient
from neuralbrewery.core.config import (
    AgentSettings,
    ClaudeSettings,
    OpenAICompatSettings,
    PlantSettings,
    ServerSettings,
    Settings,
)
from neuralbrewery.core.plant.dependencies import PLANT_READER
from neuralbrewery.core.plant.protocols import (
    PlantCommander,
    PlantReader,
    SimulationControl,
)
from neuralbrewery.features.agents.router import PLANT_AGENT
from neuralbrewery.main import create_app

SRC = Path(neuralbrewery.__file__).parent

# The one module that may name the commander, besides core/plant/protocols.py,
# which defines it
MAY_NAME_THE_COMMANDER = {Path("features/approvals/api/executor.py")}


def names_in(path: Path) -> set[str]:
    """Every name a module uses, imports included: not its comments."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.id if isinstance(node, ast.Name) else node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Name | ast.Attribute)
    } | {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }


def stored(simulation_control: bool) -> list[object]:
    """Everything create_app puts in app.state."""
    app = create_app(
        Settings(
            server=ServerSettings(trusted_hosts=["testserver"]),
            plant=PlantSettings(simulation_control=simulation_control),
        )
    )
    return list(vars(app.state)["_state"].values())


class TestOnlyTheExecutorCommands:
    def test_only_the_executor_names_the_commander(self):
        """[SEC] By name: no other module imports, types or refers to it."""
        naming = {
            path.relative_to(SRC)
            for path in SRC.rglob("*.py")
            if "PlantCommander" in names_in(path)
        }

        assert naming == MAY_NAME_THE_COMMANDER

    @pytest.mark.parametrize("simulation_control", [False, True])
    def test_nothing_in_app_state_can_command(self, simulation_control):
        """[SEC] At run time: no object in app.state has the buttons."""
        commanders = [
            value
            for value in stored(simulation_control)
            if isinstance(value, PlantCommander)
        ]

        assert commanders == []

    def test_whoever_reads_holds_a_reader_and_nothing_else(self, settings):
        """[SEC] The reader in app.state cannot command or move the time."""
        reader = PLANT_READER.get(create_app(settings).state)

        assert isinstance(reader, PlantReader)
        assert not isinstance(reader, PlantCommander)
        assert not isinstance(reader, SimulationControl)


class TestSimulationOnlyWhenAsked:
    def test_off_nothing_moves_the_time(self):
        """[SEC] The default: no object in app.state can move time or break."""
        assert not [v for v in stored(False) if isinstance(v, SimulationControl)]

    def test_on_the_hand_of_the_test_and_no_more(self):
        """[HP] On: one object moves the time, and it cannot read or command."""
        [control] = [v for v in stored(True) if isinstance(v, SimulationControl)]

        assert not isinstance(control, PlantReader)
        assert not isinstance(control, PlantCommander)


def with_keys(provider: str, *, claude_key: str = "", compat_key: str = "") -> Settings:
    return Settings(
        server=ServerSettings(trusted_hosts=["testserver"]),
        agent=AgentSettings(provider=provider),
        claude=ClaudeSettings(api_key=claude_key),
        openai_compat=OpenAICompatSettings(api_key=compat_key),
    )


class TestThePlantAgent:
    @pytest.mark.parametrize(
        ("provider", "client_class"),
        [("claude", ClaudeClient), ("openai_compat", OpenAICompatClient)],
    )
    def test_with_a_key_the_agent_reads_and_nothing_more(self, provider, client_class):
        """[SEC] Either provider: an agent on its client, holding a reader alone."""
        settings = with_keys(provider, claude_key="sk-ant-test", compat_key="gm-test")

        agent = PLANT_AGENT.get(create_app(settings).state)

        assert isinstance(agent._client, client_class)
        assert isinstance(agent.reader, PlantReader)
        assert not isinstance(agent.reader, PlantCommander)
        assert not isinstance(agent.reader, SimulationControl)

    def test_without_a_key_there_is_no_agent(self, settings):
        """[EC] The default: the endpoint answers 503 (tests/features/agents)."""
        with pytest.raises(AttributeError):
            PLANT_AGENT.get(create_app(settings).state)

    # The settings are built in the test, after the autouse fixture has
    # switched off the environment: not here, when the module is collected
    @pytest.mark.parametrize(
        ("provider", "keys"),
        [
            ("openai_compat", {"claude_key": "sk-ant-test"}),
            ("claude", {"compat_key": "gm-test"}),
        ],
        ids=["second-chosen-claude-key", "claude-chosen-second-key"],
    )
    def test_only_the_key_of_the_chosen_provider_counts(self, provider, keys):
        """[EC] The key of the other provider does not make an agent: 503."""
        with pytest.raises(AttributeError):
            PLANT_AGENT.get(create_app(with_keys(provider, **keys)).state)
