"""The M5 eval: the plant agent, on the real Claude, on three fault scenarios.

Under test: src/neuralbrewery/features/agents/ with adapters/claude/, on
the simulated plant in process. Run by hand: uv run pytest -m eval

WHY this eval exists: the tests with a scripted client prove the code
around the model; only the model can show whether the diagnoses are right.
The scenarios and their checks are in scenarios.py.
"""

import pytest

from neuralbrewery.adapters.claude.client import generation_args
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.features.agents.plant_agent import PlantAgent
from tests.evals.scenarios import SCENARIOS, Scenario, grade


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda scenario: scenario.name)
async def test_the_agent_diagnoses(scenario: Scenario, claude, claude_settings, record):
    plant = await scenario.prepare()
    reader: PlantReader = plant

    run = await PlantAgent(reader, claude, generation_args(claude_settings)).diagnose()

    failures = grade(scenario, run)
    record(scenario.name, scenario.title, run, failures)
    assert not failures, failures
