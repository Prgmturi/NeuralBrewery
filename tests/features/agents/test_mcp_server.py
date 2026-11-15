"""Tests for the MCP server: four tools that read the plant, one that proposes.

Module under test: src/neuralbrewery/features/agents/mcp_server.py
Layer: The tools as an MCP client sees them, in process, no network

WHY these tests exist: Claude Code, or any MCP client, reaches the plant
through this server. It may read and propose, never approve or command:
what it proposes goes into the queue as from "mcp", out of limits it is
blocked with the reason, and nothing it gets back carries real time
(AGENTS.md, rule 5) or the approval token.
"""

import inspect
import json
from collections.abc import Mapping
from typing import Any
from uuid import UUID

import pytest
from mcp import Client

from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.starts import brew_day
from neuralbrewery.core.approvals.schemas import Actor, Receipt
from neuralbrewery.core.plant.panel import Command
from neuralbrewery.features.agents.mcp_server import create_mcp_server

PROPOSAL_ID = UUID("6f1c2a5e-0000-4000-8000-000000000001")
READING = {"read_plant", "read_events", "read_history", "run_watcher"}


class RecordingInbox:
    """The ProposalInbox port: records each proposal, answers as told."""

    def __init__(self, receipt: Receipt | None = None) -> None:
        self.proposals: list[tuple[str, dict[str, Any], Actor, str, str]] = []
        self._receipt = receipt or Receipt(PROPOSAL_ID, "proposed")

    async def propose(
        self,
        command: str,
        arguments: Mapping[str, Any],
        actor: Actor,
        by: str,
        why: str,
    ) -> Receipt:
        self.proposals.append((command, dict(arguments), actor, by, why))
        return self._receipt


@pytest.fixture
def plant() -> InProcessPlant:
    return InProcessPlant(brew_day())


@pytest.fixture
def inbox() -> RecordingInbox:
    return RecordingInbox()


@pytest.fixture
def mcp(plant, inbox):
    """The server; each helper below opens a client of its own.

    Not a client in a fixture: anyio wants it closed in the task that
    opened it, and pytest tears fixtures down in another.
    """
    return create_mcp_server(plant, inbox)


async def tools_of(server) -> dict:
    async with Client(server) as client:
        return {tool.name: tool for tool in (await client.list_tools()).tools}


async def text_of(server, tool: str, **arguments: Any) -> str:
    async with Client(server) as client:
        result = await client.call_tool(tool, arguments)
    assert not result.is_error, result.content
    return result.content[0].text


class TestTools:
    async def test_four_read_and_one_proposes(self, mcp):
        """[SEC] No tool approves, rejects or presses a button."""
        assert set(await tools_of(mcp)) == READING | {"propose_action"}

    async def test_the_arguments_say_what_they_are(self, mcp):
        """[HP] The model reads a description of each argument, as datapizza's does."""
        tools = await tools_of(mcp)

        history = tools["read_history"].input_schema["properties"]
        assert "sigla" in history["tag"]["description"]
        assert "minuti" in history["since_minutes"]["description"]
        propose = tools["propose_action"].input_schema["properties"]
        assert set(propose) == {"command", "arguments", "why"}
        assert all(field["description"] for field in propose.values())

    async def test_read_plant_is_the_controller_now(self, mcp):
        """[HP] The same snapshot the agent reads: simulated time, no alarm."""
        plant = json.loads(await text_of(mcp, "read_plant"))

        assert plant["sim_time_s"] == 0
        assert plant["alarms"] == []

    async def test_the_other_readings(self, mcp):
        """[HP] Events, history and the watcher answer in JSON."""
        assert json.loads(await text_of(mcp, "read_events")) == []
        history = json.loads(await text_of(mcp, "read_history", tag="TT1"))
        assert history["tag"] == "TT1"
        assert json.loads(await text_of(mcp, "run_watcher")) == []

    async def test_an_unknown_tag_is_an_answer(self, mcp):
        """[EC] Not an error: a sentence the model can act on."""
        assert "Nessuno storico" in await text_of(mcp, "read_history", tag="XX9")


class TestPropose:
    async def test_drops_the_proposal_in_the_inbox_as_mcp(self, mcp, inbox):
        """[HP] Command, arguments and why reach the queue, from "mcp"."""
        answer = await text_of(
            mcp,
            "propose_action",
            command="set_temperature",
            arguments={"vessel": "FERM", "celsius": 18.0},
            why="TT5a legge due gradi in più",
        )

        assert inbox.proposals == [
            (
                "set_temperature",
                {"vessel": "FERM", "celsius": 18.0},
                Actor.MCP,
                "mcp",
                "TT5a legge due gradi in più",
            )
        ]
        assert json.loads(answer) == {
            "proposal_id": str(PROPOSAL_ID),
            "status": "proposed",
            "reason": "",
        }

    async def test_a_button_with_no_arguments(self, mcp, inbox):
        """[HP] arguments and why may be left out."""
        await text_of(mcp, "propose_action", command="reset")

        assert inbox.proposals == [("reset", {}, Actor.MCP, "mcp", "")]

    async def test_a_blocked_proposal_is_an_answer(self, plant):
        """[EC] Out of limits: the reason comes back as a result, not an error."""
        receipt = Receipt(PROPOSAL_ID, "blocked", "Il setpoint di FERM va da 0 a 30")
        server = create_mcp_server(plant, RecordingInbox(receipt))

        answer = json.loads(
            await text_of(
                server,
                "propose_action",
                command="set_temperature",
                arguments={"vessel": "FERM", "celsius": 45},
            )
        )

        assert answer["status"] == "blocked"
        assert "30" in answer["reason"]

    async def test_the_description_lists_every_button(self, mcp):
        """[HP] The model learns the buttons and what each one takes."""
        tools = await tools_of(mcp)
        description = tools["propose_action"].description

        assert all(command.value in description for command in Command)
        assert "set_temperature(vessel, celsius?)" in description


def test_the_server_gets_a_reader_and_an_inbox_and_nothing_else():
    """[SEC] No settings, so no token; no executor, so no button."""
    assert list(inspect.signature(create_mcp_server).parameters) == ["reader", "inbox"]
