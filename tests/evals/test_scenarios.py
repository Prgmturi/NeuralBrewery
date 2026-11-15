"""The eval: the plant agent, on a real model, on the fault scenarios.

Under test: src/neuralbrewery/features/agents/ with the adapter of
AGENT_PROVIDER (adapters/claude/ or adapters/openai_compat/), on the
simulated plant in process. Run by hand: uv run pytest -m eval, with
AGENT_PROVIDER=openai_compat for the second provider.

WHY this eval exists: the tests with a scripted client prove the code
around the model; only the model can show whether the diagnoses are right,
and how two providers compare on the same scenarios. The scenarios and
their checks are in scenarios.py.
"""

import pytest

from neuralbrewery.core.exceptions import AppExceptionError
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.features.agents.diagnosis import DiagnosisRun, Outcome
from neuralbrewery.features.agents.plant_agent import PlantAgent
from tests.evals.scenarios import SCENARIOS, Scenario, grade


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda scenario: scenario.name)
async def test_the_agent_diagnoses(scenario: Scenario, model, record):
    client, generation = model
    plant = await scenario.prepare()
    reader: PlantReader = plant

    try:
        run = await PlantAgent(reader, client, generation).diagnose()
    except AppExceptionError as error:
        # 503 or 502 from the adapter: a result for the table, not a crash
        run = DiagnosisRun(
            outcome=Outcome.NO_DIAGNOSIS,
            diagnosis=None,
            detail=f"{error.status_code} {error.message}",
            steps=(),
        )

    failures = grade(scenario, run)
    record(scenario.name, scenario.title, run, failures)
    assert not failures, failures
