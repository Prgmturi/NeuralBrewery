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

from neuralbrewery.adapters.manuals.index import ManualIndex
from neuralbrewery.core.exceptions import AppExceptionError
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.features.agents.diagnosis import DiagnosisRun, Outcome
from neuralbrewery.features.agents.plant_agent import PlantAgent
from tests.evals.scenarios import (
    SCENARIOS,
    RememberedDecisions,
    Scenario,
    citation,
    grade,
)


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda scenario: scenario.name)
async def test_the_agent_diagnoses(scenario: Scenario, model, record, manuals_settings):
    client, generation = model
    plant = await scenario.prepare()
    reader: PlantReader = plant
    memory = RememberedDecisions(scenario.decisions)  # empty, but for S5
    # As the app: MANUALS_ENABLED exported, or S6, which is about them
    on = scenario.manuals or manuals_settings.enabled
    manuals = ManualIndex.from_folder(manuals_settings.folder) if on else None

    try:
        run = await PlantAgent(
            reader, memory, client, generation, manuals=manuals
        ).diagnose()
    except AppExceptionError as error:
        # 503 or 502 from the adapter: a result for the table, not a crash
        run = DiagnosisRun(
            outcome=Outcome.NO_DIAGNOSIS,
            diagnosis=None,
            detail=f"{error.status_code} {error.message}",
            steps=(),
        )

    failures = grade(scenario, run)
    remarks = (
        (f"citazione del manuale (V20, pagina 55): {citation(run.diagnosis)}",)
        if scenario.manuals
        else ()
    )
    record(scenario.name, scenario.title, run, failures, manuals=on, remarks=remarks)
    assert not failures, failures
