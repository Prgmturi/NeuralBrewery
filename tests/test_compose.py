"""Tests for compose.yaml, the whole stack started with docker compose up.

WHY these tests exist: from a clean clone docker compose up answered "no
configuration file provided". And the compose files fixed the names of
their containers, networks and volumes, so a second project made from
the template would have used the first one's database volume. tests/e2e/
runs the demo through the running stack.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
COMPOSE = ROOT / "compose.yaml"


@dataclass
class Tag:
    """A Compose tag such as !reset or !override, with its value."""

    name: str
    value: object


class ComposeLoader(yaml.SafeLoader):
    """yaml.safe_load, plus the tags Compose adds to YAML."""


def construct_tag(loader: ComposeLoader, suffix: str, node: yaml.Node) -> Tag:
    if isinstance(node, yaml.SequenceNode):
        return Tag(suffix, loader.construct_sequence(node, deep=True))
    if isinstance(node, yaml.MappingNode):
        return Tag(suffix, loader.construct_mapping(node, deep=True))
    return Tag(suffix, loader.construct_scalar(node))


ComposeLoader.add_multi_constructor("!", construct_tag)


def services() -> dict:
    return yaml.safe_load(COMPOSE.read_text())["services"]


def compose_files() -> list[Path]:
    """Every compose file of the repository."""
    return [
        path
        for pattern in ("compose*.yaml", "*/docker-compose.y*ml")
        for path in ROOT.glob(pattern)
    ]


def env_example(name: str) -> str:
    match = re.search(rf"^{name}=(.*)$", (ROOT / ".env.example").read_text(), re.M)
    assert match is not None, name
    return match.group(1)


class TestStack:
    def test_one_file_starts_everything(self):
        """[HP] API, migrations, Postgres, the dashboard: no login service.

        WHY: Keycloak took up to 5 minutes on its first start, and the demo
        never used it (gone in M10).
        """
        assert set(services()) == {"api", "migrate", "db", "dashboard"}

    def test_no_fixed_names(self):
        """[HP] Compose derives every name from the project.

        WHY: a fixed volume name is shared by every project that uses it,
        so a second clone, or a second project made from the template,
        would start on the first one's database.
        """
        fixed = [
            f"{path.name}: {section} {key}"
            for path in compose_files()
            for section, entries in yaml.load(path.read_text(), ComposeLoader).items()
            if isinstance(entries, dict)
            for key, entry in entries.items()
            if isinstance(entry, dict) and {"container_name", "name"} & set(entry)
        ]

        assert compose_files()
        assert fixed == []

    def test_api_starts_after_migrations(self):
        """[HP] The API waits for the schema: requests need its tables."""
        assert services()["api"]["depends_on"] == {
            "db": {"condition": "service_healthy"},
            "migrate": {"condition": "service_completed_successfully"},
        }
        assert services()["migrate"]["command"] == ["alembic", "upgrade", "head"]
        assert services()["migrate"]["depends_on"] == {
            "db": {"condition": "service_healthy"}
        }

    def test_every_port_answers_on_this_machine_only(self):
        """[SEC] Nobody on the same network reaches a service of the stack.

        WHY: Postgres (5433) was published on every interface, with the
        password written in this file: on the Wi-Fi of the room of the
        speech, anyone could open the queue with psql (decided on 16
        November). The API and the dashboard already were on the loopback.
        Inside the stack nothing changes: the API calls db:5432, and the
        browser calls localhost.
        """
        published = {
            name: service["ports"]
            for name, service in services().items()
            if "ports" in service
        }

        assert set(published) == {"api", "dashboard", "db"}
        assert [
            f"{name}: {port}"
            for name, ports in published.items()
            for port in ports
            if not port.startswith("127.0.0.1:")
        ] == []

    def test_the_host_calls_the_database_on_ipv4(self):
        """[EC] .env.example names 127.0.0.1, where the stack publishes Postgres.

        WHY: on Windows, localhost is ::1 first, and a port published on
        127.0.0.1 only answers there after about 2 s of retries: 2.1 to
        2.3 s for each new connection of alembic, of the integration tests
        and of the app on the host, against 0.002 s on 127.0.0.1 (measured
        on 16 November 2026).
        """
        assert env_example("DATABASE_HOST") == "127.0.0.1"
        assert env_example("TEST_DATABASE_HOST") == "127.0.0.1"


class TestPlantInTheApi:
    """The plant lives in the api service until M2 (docs/decisioni.md)."""

    def test_development_can_move_time_and_approve(self):
        """[HP] The demo moves time and approves with the token of .env.example."""
        api = services()["api"]["environment"]

        assert api["PLANT_SIMULATION_CONTROL"] == "true"
        assert api["APPROVAL_TOKEN"] == env_example("APPROVAL_TOKEN")

    def test_the_key_of_claude_comes_from_the_host(self):
        """[SEC] The key is read from .env or the shell, never written here."""
        api = services()["api"]["environment"]

        assert api["ANTHROPIC_API_KEY"] == "${ANTHROPIC_API_KEY:-}"

    def test_the_manuals_are_on_unless_switched_off(self):
        """[HP] On by default; MANUALS_ENABLED=false from .env or the shell.

        WHY: after the evals of M9, and with the parameter list of the V20
        fixed by hand, the demo runs with the manuals. A .env written
        before M9 has no such line: compose turns them on all the same.
        """
        api = services()["api"]["environment"]

        assert api["MANUALS_ENABLED"] == "${MANUALS_ENABLED:-true}"
        assert env_example("MANUALS_ENABLED") == "true"

    def test_development_answers_on_this_machine_only(self):
        """[SEC] Nobody on the same network reaches the API of the demo.

        WHY: in development the simulation routes are open, /mcp and the
        agent ask for no login, and the approval token is public: on the
        Wi-Fi of the room of the speech, anyone could break the plant or
        approve (decided on 15 November).
        """
        ports = services()["api"]["ports"]

        assert ports
        assert all(port.startswith("127.0.0.1:") for port in ports)


class TestDashboard:
    """The brewer's dashboard, the page the demo runs from (docs/decisioni.md)."""

    def test_its_own_image(self):
        """[HP] Not the API's: Streamlit stays out of the image of the API."""
        assert services()["dashboard"]["build"]["dockerfile"] == (
            "docker/dashboard.Dockerfile"
        )

    def test_reaches_the_api_inside_the_stack_with_its_token(self):
        """[HP] As "api", with the token the API expects and .env.example holds."""
        dashboard = services()["dashboard"]["environment"]
        api = services()["api"]["environment"]

        assert dashboard["DASHBOARD_API_URL"] == "http://api:8000"
        assert dashboard["DASHBOARD_APPROVAL_TOKEN"] == api["APPROVAL_TOKEN"]
        assert env_example("DASHBOARD_APPROVAL_TOKEN") == api["APPROVAL_TOKEN"]

    def test_the_api_answers_to_the_name_it_is_called_by(self):
        """[EC] TrustedHostMiddleware answers 400 to a host it does not list."""
        hosts = json.loads(services()["api"]["environment"]["SERVER_TRUSTED_HOSTS"])

        assert "api" in hosts
        assert hosts[0] == "localhost"  # the Host of the image's health probe

    def test_on_the_loopback_only_in_development_too(self):
        """[SEC] The page holds the token: nobody on the room's Wi-Fi reaches it."""
        ports = services()["dashboard"]["ports"]

        assert ports
        assert all(port.startswith("127.0.0.1:") for port in ports)

    def test_starts_once_the_api_is_healthy(self):
        """[HP] Its first page asks the API for the plant."""
        assert services()["dashboard"]["depends_on"] == {
            "api": {"condition": "service_healthy"}
        }
