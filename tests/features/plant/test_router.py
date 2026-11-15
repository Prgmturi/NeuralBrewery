"""Tests for the routes of the plant and of the simulation.

Module under test: src/neuralbrewery/features/plant/router.py
Layer: FastAPI routes, on the plant that create_app builds in the process

WHY these tests exist: until M2 the plant lives in the API, and the demo
moves its time and breaks it through these routes. They must show what
the controller shows, and exist only when PLANT_SIMULATION_CONTROL is on:
staging and production refuse it, and anyone could break the plant.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from neuralbrewery.core.config import PlantSettings, ServerSettings, Settings
from neuralbrewery.main import create_app
from tests.test_exception_handlers import assert_problem

HOUR = 3600


def settings_with(**plant: object) -> Settings:
    return Settings(
        server=ServerSettings(trusted_hosts=["testserver"]),
        plant=PlantSettings(**plant),
    )


@pytest.fixture
def settings() -> Settings:
    """The test settings, with the routes of the simulation."""
    return settings_with(simulation_control=True)


async def get(settings: Settings, path: str):
    """One GET on a new app built from these settings."""
    app = create_app(settings)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        return await client.get(path)


class TestPlant:
    async def test_shows_what_the_controller_shows(self, client):
        """[HP] The brew day at its start: time 0, program idle, no alarm."""
        response = await client.get("/plant")

        assert response.status_code == 200
        plant = response.json()
        assert plant["sim_time_s"] == 0
        assert plant["program"]["status"] == "idle"
        assert plant["alarms"] == []
        assert plant["readings"]["LT1"]["unit"] == "L"

    async def test_the_start_comes_from_the_settings(self):
        """[HP] PLANT_START=fermentation: the fermenter is held at 19 °C."""
        response = await get(settings_with(start="fermentation"), "/plant")

        assert response.json()["regulation"]["FERM"]["setpoint_c"] == 19.0


class TestSimulation:
    async def test_advance_moves_time_and_says_what_happened(self, client):
        """[HP] One hour on: the new time, the alarms and the watcher's judgements."""
        response = await client.post("/simulation/advance", json={"seconds": HOUR})

        assert response.status_code == 200
        body = response.json()
        assert body == {"sim_time_s": HOUR, "alarms": [], "judgements": []}
        assert (await client.get("/plant")).json()["sim_time_s"] == HOUR

    async def test_a_fault_shows_in_the_alarms(self, client):
        """[HP] A broken PT100 in the HLT: the controller raises signal_fault."""
        injected = await client.post(
            "/simulation/faults", json={"kind": "probe_broken", "target": "TT1"}
        )
        advanced = await client.post("/simulation/advance", json={"seconds": 60})

        assert injected.status_code == 204
        alarms = advanced.json()["alarms"]
        assert [(a["code"], a["tag"]) for a in alarms] == [("signal_fault", "TT1")]

    async def test_clearing_the_faults_mends_the_instruments(self, client):
        """[HP] Cleared, the probe reads again and its alarm ends."""
        await client.post(
            "/simulation/faults", json={"kind": "probe_broken", "target": "TT1"}
        )
        await client.post("/simulation/advance", json={"seconds": 60})

        cleared = await client.delete("/simulation/faults")
        advanced = await client.post("/simulation/advance", json={"seconds": 60})

        assert cleared.status_code == 204
        assert advanced.json()["alarms"] == []

    async def test_a_fault_the_target_cannot_have_is_refused(self, client):
        """[EC] A pump cannot have a broken probe: 422, from the simulator."""
        response = await client.post(
            "/simulation/faults", json={"kind": "probe_broken", "target": "P1"}
        )

        assert_problem(response, 422)

    @pytest.mark.parametrize(
        "seconds", [0, -60, 24 * HOUR + 1], ids=["zero", "back", "over-a-day"]
    )
    async def test_time_moves_forward_a_day_at_most(self, client, seconds):
        """[EC] 422: an hour of brew day blocks the API for about 0.16 s."""
        response = await client.post("/simulation/advance", json={"seconds": seconds})

        assert_problem(response, 422)

    async def test_time_moves_by_whole_steps(self, client):
        """[EC] Half a second on a brew day of 1 s steps: 422, from the simulator."""
        response = await client.post("/simulation/advance", json={"seconds": 0.5})

        assert_problem(response, 422)


class TestClosedUnlessAskedFor:
    """PLANT_SIMULATION_CONTROL off, the default and production's only value."""

    @pytest.mark.parametrize(
        ("method", "path"),
        [
            ("POST", "/simulation/advance"),
            ("POST", "/simulation/faults"),
            ("DELETE", "/simulation/faults"),
        ],
    )
    async def test_the_routes_do_not_exist(self, method, path):
        """[SEC] 404: no route moves the time or breaks the plant."""
        app = create_app(settings_with())
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            response = await client.request(method, path, json={"seconds": 60})

        assert_problem(response, 404)

    def test_the_schema_does_not_show_them(self):
        """[SEC] Not even documented."""
        paths = create_app(settings_with()).openapi()["paths"]

        assert "/plant" in paths
        assert not [path for path in paths if path.startswith("/simulation")]
