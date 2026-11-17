"""Tests for compose.yaml, the whole stack started with docker compose up.

WHY these tests exist: from a clean clone docker compose up answered "no
configuration file provided". Starting the app took three .env files, two
compose files and six steps by hand in Keycloak's console. And the
compose files fixed the names of their containers, networks and volumes,
so a second project made from this template would have used the first
one's database volume. tests/e2e/ logs in through the running stack.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pydantic
import pytest
import yaml

from neuralbrewery.core.config import KeycloakSettings, Settings

ROOT = Path(__file__).parent.parent
COMPOSE = ROOT / "compose.yaml"
DEV_REALM = ROOT / "docker" / "keycloak" / "realm-dev.json"
REALM_IMPORT_DIR = "/opt/keycloak/data/import/"


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


def realm() -> dict:
    return json.loads(DEV_REALM.read_text())


def backend_client() -> dict:
    """The client of the realm that the API logs users in with."""
    client_id = KeycloakSettings().client_id
    return next(c for c in realm()["clients"] if c["clientId"] == client_id)


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
        """[HP] API, migrations, Postgres, Keycloak and its Postgres, the dashboard."""
        assert set(services()) == {
            "api",
            "migrate",
            "db",
            "keycloak",
            "keycloak-db",
            "dashboard",
        }

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

    def test_api_starts_after_migrations_and_keycloak(self):
        """[HP] The API waits for the schema and for Keycloak's keys.

        WHY: the startup fetches Keycloak's signing keys and fails if
        Keycloak is not ready; requests need the tables of the migrations.
        """
        assert services()["api"]["depends_on"] == {
            "db": {"condition": "service_healthy"},
            "migrate": {"condition": "service_completed_successfully"},
            "keycloak": {"condition": "service_healthy"},
        }
        assert services()["migrate"]["command"] == ["alembic", "upgrade", "head"]
        assert services()["migrate"]["depends_on"] == {
            "db": {"condition": "service_healthy"}
        }

    def test_keycloak_has_time_for_a_slow_first_start(self):
        """[EC] compose up --wait waits for a Keycloak that starts slowly.

        WHY: on a busy laptop its first start, with the realm imported and
        its schema created, took 417 s, while its probes gave up after
        about 160 s: compose up --wait stopped with "keycloak is unhealthy"
        and the API never started (16 November 2026). In CI the whole stack
        starts in 2 minutes. Failed probes do not count during start_period,
        and the first one that passes makes it healthy: a fast machine
        waits no longer.
        """
        health = services()["keycloak"]["healthcheck"]

        assert int(health["start_period"].removesuffix("s")) >= 300

    def test_every_port_answers_on_this_machine_only(self):
        """[SEC] Nobody on the same network reaches a service of the stack.

        WHY: Postgres (5433) and Keycloak (8080) were published on every
        interface, with the passwords written in this file: on the Wi-Fi
        of the room of the speech, anyone could open the queue with psql,
        or ask Keycloak for an administrator's token with admin/admin
        (decided on 16 November). The API and the dashboard already were
        on the loopback. Inside the stack nothing changes: the API calls
        db:5432 and keycloak:8080, and the browser calls localhost.
        """
        published = {
            name: service["ports"]
            for name, service in services().items()
            if "ports" in service
        }

        assert set(published) == {"api", "dashboard", "db", "keycloak"}
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
        on 16 November 2026). Keycloak stays localhost: the issuer of its
        tokens is http://localhost, and the API compares the two.
        """
        assert env_example("DATABASE_HOST") == "127.0.0.1"
        assert env_example("TEST_DATABASE_HOST") == "127.0.0.1"
        assert env_example("KEYCLOAK_HOST") == "localhost"


class TestDevRealm:
    """The realm Keycloak imports, and the API settings that match it."""

    def test_keycloak_imports_the_realm(self):
        """[HP] start-dev with --import-realm, and the file in the import folder."""
        keycloak = services()["keycloak"]

        assert keycloak["command"] == ["start-dev", "--import-realm"]
        assert any(
            volume.startswith("./docker/keycloak/realm-dev.json:" + REALM_IMPORT_DIR)
            for volume in keycloak["volumes"]
        )

    def test_realm_and_client_are_the_api_defaults(self):
        """[HP] The realm and the client the API uses unless told otherwise."""
        assert realm()["realm"] == KeycloakSettings().realm
        assert backend_client()["publicClient"] is False

    def test_api_has_the_client_secret_of_the_realm(self):
        """[HP] One development secret: the realm's, the API's, .env.example's."""
        secret = backend_client()["secret"]

        assert services()["api"]["environment"]["KEYCLOAK_CLIENT_SECRET"] == secret
        assert env_example("KEYCLOAK_CLIENT_SECRET") == secret

    def test_issuer_is_the_address_of_the_browser(self):
        """[HP] Tokens name the address the browser uses, the one the API expects.

        WHY: the API reaches Keycloak at http://keycloak:8080, the browser at
        localhost. Keycloak names KC_HOSTNAME as issuer; the API compares it
        with KEYCLOAK_PUBLIC_URL and answers 401 Invalid issuer otherwise
        (measured with a real Keycloak on 20 October 2026).
        """
        keycloak = services()["keycloak"]["environment"]
        api = services()["api"]["environment"]

        assert keycloak["KC_HOSTNAME"] == api["KEYCLOAK_PUBLIC_URL"]
        assert keycloak["KC_HOSTNAME_BACKCHANNEL_DYNAMIC"] == "true"
        assert api["KEYCLOAK_HOST"] == "keycloak"

    def test_production_refuses_the_dev_secret(self, production_env, monkeypatch):
        """[SEC] The secret of the dev realm is public: production stops on it."""
        monkeypatch.setenv("KEYCLOAK_CLIENT_SECRET", backend_client()["secret"])

        with pytest.raises(pydantic.ValidationError) as exc_info:
            Settings()

        assert "KEYCLOAK_CLIENT_SECRET" in str(exc_info.value)


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
