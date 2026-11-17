"""Tests for settings — configuration loading, URL construction, defaults.

Module under test: src/neuralbrewery/core/config/
Layer: Pure domain (Pydantic settings)

WHY these tests exist: Configuration errors are silent and catastrophic.
We verify defaults, what each variable changes, what production refuses,
and that security-sensitive fields are masked.
"""

import importlib.metadata
from pathlib import Path

import pydantic
import pytest

from neuralbrewery.core.config import Settings
from neuralbrewery.core.config import app as app_module
from neuralbrewery.core.config.agent import AgentSettings
from neuralbrewery.core.config.app import AppSettings
from neuralbrewery.core.config.approvals import ApprovalSettings
from neuralbrewery.core.config.claude import ClaudeSettings
from neuralbrewery.core.config.database import DatabaseSettings
from neuralbrewery.core.config.manuals import ManualsSettings
from neuralbrewery.core.config.openai_compat import OpenAICompatSettings
from neuralbrewery.core.config.plant import PlantSettings
from neuralbrewery.core.config.server import ServerSettings
from tests.conftest import SETTINGS_CLASSES

ENV_EXAMPLE = Path(__file__).parents[3] / ".env.example"


class TestAppSettings:
    """AppSettings — application metadata and environment detection.

    WHY: is_development/is_production control docs visibility and
    debug behavior. Wrong detection = docs exposed in production.
    """

    def test_default_values(self):
        """[HP] Defaults are development-friendly."""
        settings = AppSettings()
        assert settings.name == "neuralbrewery"
        assert settings.environment == "development"
        assert settings.debug is False

    def test_version_is_the_installed_package(self):
        """[HP] /health/live and OpenAPI show the version that runs.

        WHY: the default was "0.1.0" in the code and in .env.example, while
        the version lives in pyproject.toml: a new version would still have
        answered 0.1.0.
        """
        assert AppSettings().version == importlib.metadata.version("neuralbrewery")

    def test_version_unknown_without_an_installed_package(self, monkeypatch):
        """[EC] Source on PYTHONPATH, never installed: "unknown", not a crash."""

        def not_installed(name: str) -> str:
            raise importlib.metadata.PackageNotFoundError(name)

        monkeypatch.setattr(app_module, "package_version", not_installed)

        assert AppSettings().version == "unknown"

    def test_app_version_still_overrides(self, monkeypatch):
        """[HP] APP_VERSION, for a build that wants its own label."""
        monkeypatch.setenv("APP_VERSION", "1.2.3-rc1")

        assert AppSettings().version == "1.2.3-rc1"

    def test_is_development_true_in_dev(self):
        """[HP] environment='development' -> is_development=True."""
        settings = AppSettings(environment="development")
        assert settings.is_development is True

    def test_is_development_false_in_production(self):
        """[EC] environment='production' -> is_development=False."""
        settings = AppSettings(environment="production")
        assert settings.is_development is False

    def test_is_production_true_in_production(self):
        """[HP] environment='production' -> is_production=True."""
        settings = AppSettings(environment="production")
        assert settings.is_production is True

    @pytest.mark.parametrize("given", ["debug", "Debug", "DEBUG"])
    def test_log_level_any_case(self, given):
        """[HP] APP_LOG_LEVEL=debug works like DEBUG."""
        assert AppSettings(log_level=given).log_level == "DEBUG"

    def test_log_level_read_from_the_environment(self, monkeypatch):
        """[HP] APP_LOG_LEVEL, as written in .env."""
        monkeypatch.setenv("APP_LOG_LEVEL", "warning")

        assert AppSettings().log_level == "WARNING"

    @pytest.mark.parametrize("given", ["verbose", "WARN ", "root"])
    def test_log_level_typo_refused(self, given):
        """[EC] An unknown level stops the startup.

        WHY: getattr(logging, level, logging.INFO) turned a typo into INFO
        without a word, and "root" into a Logger object.
        """
        with pytest.raises(pydantic.ValidationError, match="DEBUG"):
            AppSettings(log_level=given)


class TestClaudeSettings:
    """ClaudeSettings: the model of the agents and the budget of each call.

    WHY: the defaults are the choices of docs/decisioni.md (claude-sonnet-5-5,
    effort high). datapizza falls back to 2048 tokens per call, which thinking
    and answer share: a diagnosis could end half way.
    """

    def test_defaults(self):
        """[HP] Sonnet, 16000 tokens, effort high, and no key."""
        settings = ClaudeSettings()

        assert settings.model == "claude-sonnet-5-5"
        assert settings.max_tokens == 16000
        assert settings.effort == "high"
        assert settings.api_key.get_secret_value() == ""

    def test_read_from_the_environment(self, monkeypatch):
        """[HP] The key under the name of the Anthropic tools, the rest as CLAUDE_*."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-from-the-env")
        monkeypatch.setenv("CLAUDE_MODEL", "claude-opus-5-5")
        monkeypatch.setenv("CLAUDE_EFFORT", "medium")

        settings = ClaudeSettings()

        assert settings.api_key.get_secret_value() == "sk-ant-from-the-env"
        assert (settings.model, settings.effort) == ("claude-opus-5-5", "medium")

    def test_anthropic_model_of_other_tools_is_ignored(self, monkeypatch):
        """[EC] Claude Code exports ANTHROPIC_MODEL: it must not pick our model."""
        monkeypatch.setenv("ANTHROPIC_MODEL", "claude-haiku-5-5")

        assert ClaudeSettings().model == "claude-sonnet-5-5"

    @pytest.mark.parametrize("given", ["highest", "HIGH", ""])
    def test_effort_typo_refused(self, given):
        """[EC] An effort the API does not know stops the startup, not the call."""
        with pytest.raises(pydantic.ValidationError, match="effort"):
            ClaudeSettings(effort=given)


class TestAgentSettings:
    """AgentSettings: which provider the agents run on.

    WHY: the course asks for a multi-provider client (docs/decisioni.md,
    "Secondo fornitore"). Claude stays the default, and the live demo on it.
    """

    def test_claude_by_default(self):
        """[HP] Nothing set: Claude."""
        assert AgentSettings().provider == "claude"

    def test_read_from_the_environment(self, monkeypatch):
        """[HP] AGENT_PROVIDER picks the second provider."""
        monkeypatch.setenv("AGENT_PROVIDER", "openai_compat")

        assert AgentSettings().provider == "openai_compat"

    @pytest.mark.parametrize("given", ["gemini", "Claude", ""])
    def test_unknown_provider_refused(self, given):
        """[EC] A typo stops the startup, not the first diagnosis."""
        with pytest.raises(pydantic.ValidationError, match="provider"):
            AgentSettings(provider=given)


class TestOpenAICompatSettings:
    """OpenAICompatSettings: the second provider, through an API like OpenAI's.

    WHY: the defaults are the outcome of the gate of M6: Gemini's endpoint
    for the OpenAI SDK, and a model pinned, not the -latest alias, which
    moves under the evals.
    """

    def test_defaults(self):
        """[HP] Gemini Flash-Lite, and no key."""
        settings = OpenAICompatSettings()

        assert (
            settings.base_url
            == "https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        assert settings.model == "gemini-3.5-flash-lite"
        assert settings.api_key.get_secret_value() == ""

    def test_read_from_the_environment(self, monkeypatch):
        """[HP] All three as OPENAI_COMPAT_*: Groq, say, with its own key."""
        monkeypatch.setenv("OPENAI_COMPAT_BASE_URL", "https://api.groq.com/openai/v1")
        monkeypatch.setenv("OPENAI_COMPAT_MODEL", "llama-4-scout")
        monkeypatch.setenv("OPENAI_COMPAT_API_KEY", "gsk-from-the-env")

        settings = OpenAICompatSettings()

        assert settings.base_url == "https://api.groq.com/openai/v1"
        assert settings.model == "llama-4-scout"
        assert settings.api_key.get_secret_value() == "gsk-from-the-env"


class TestPlantSettings:
    """PlantSettings: the plant the API holds, and whether time can be moved.

    WHY: the plant lives in the process of the API until M2. The start and
    the seed decide what the demo shows; the routes that move time and
    break the plant must stay closed unless asked for.
    """

    def test_defaults(self):
        """[HP] A brew day, seed 42, and no simulation routes."""
        settings = PlantSettings()

        assert (settings.start, settings.seed) == ("brew_day", 42)
        assert settings.simulation_control is False

    def test_read_from_the_environment(self, monkeypatch):
        """[HP] PLANT_* variables."""
        monkeypatch.setenv("PLANT_START", "fermentation")
        monkeypatch.setenv("PLANT_SEED", "7")
        monkeypatch.setenv("PLANT_SIMULATION_CONTROL", "true")

        settings = PlantSettings()

        assert (settings.start, settings.seed) == ("fermentation", 7)
        assert settings.simulation_control is True

    def test_unknown_start_refused(self):
        """[EC] A start with no name in starts.py stops the startup."""
        with pytest.raises(pydantic.ValidationError, match="start"):
            PlantSettings(start="mid_boil")


class TestManualsSettings:
    """ManualsSettings: the search over the manuals, for the plant agent (M9).

    WHY: off, the app must start as before, with no folder of manuals. On,
    an agent that finds nothing would answer as if the manuals said
    nothing: better that the app does not start, and says why.
    """

    def test_off_by_default_on_the_text_of_the_repository(self):
        """[HP] Off, and the folder that scripts/extract_manuals.py writes."""
        settings = ManualsSettings()

        assert settings.enabled is False
        assert settings.folder == Path("data/manuals/text")

    def test_read_from_the_environment(self, monkeypatch, tmp_path):
        """[HP] MANUALS_* variables."""
        (tmp_path / "v20.md").write_text("---", encoding="utf-8")
        monkeypatch.setenv("MANUALS_ENABLED", "true")
        monkeypatch.setenv("MANUALS_FOLDER", str(tmp_path))

        settings = ManualsSettings()

        assert (settings.enabled, settings.folder) == (True, tmp_path)

    def test_on_the_text_of_the_repository_is_there(self):
        """[HP] The default folder, from the root of the repository."""
        assert ManualsSettings(enabled=True).enabled is True

    @pytest.mark.parametrize("folder", ["nowhere", "empty"])
    def test_on_without_the_text_the_app_does_not_start(self, tmp_path, folder):
        """[EC] A folder missing or with no .md: an error that says what to do."""
        (tmp_path / "empty").mkdir()
        (tmp_path / "empty" / "notes.txt").write_text("", encoding="utf-8")

        with pytest.raises(pydantic.ValidationError) as error:
            ManualsSettings(enabled=True, folder=tmp_path / folder)

        message = str(error.value)
        assert "MANUALS_ENABLED is true" in message
        assert "scripts/extract_manuals.py" in message
        assert "MANUALS_ENABLED off" in message

    def test_off_no_folder_is_needed(self, tmp_path):
        """[HP] Off, the folder is not even looked at."""
        assert ManualsSettings(folder=tmp_path / "nowhere").enabled is False


class TestApprovalSettings:
    """ApprovalSettings: the token of whoever approves.

    WHY: without a secret nothing tells the brewer from a model that calls
    the endpoint by itself (docs/decisioni.md).
    """

    def test_empty_by_default(self):
        """[SEC] No token unless one is given: then nobody can approve."""
        assert ApprovalSettings().token.get_secret_value() == ""

    def test_read_from_the_environment(self, monkeypatch):
        """[HP] APPROVAL_TOKEN."""
        monkeypatch.setenv("APPROVAL_TOKEN", "from-the-env")

        assert ApprovalSettings().token.get_secret_value() == "from-the-env"


class TestDatabaseSettings:
    """DatabaseSettings — pool defaults.

    The URL is built in core/database/url.py (tests/core/database/test_url.py).
    """

    def test_default_pool_settings(self):
        """[HP] Pool defaults are reasonable (pool_size=5, etc.)."""
        settings = DatabaseSettings()
        assert settings.pool_size == 5
        assert settings.pool_max_overflow == 10
        assert settings.pool_timeout == 5
        assert settings.pool_recycle == 1800

    def test_default_timeouts(self):
        """[HP] 5 s to connect, 30 s per query.

        WHY: asyncpg has no query limit and waits 60 s for a connection.
        """
        settings = DatabaseSettings()
        assert settings.connect_timeout == 5
        assert settings.command_timeout == 30

    def test_timeouts_read_from_the_environment(self, monkeypatch):
        """[HP] DATABASE_CONNECT_TIMEOUT and DATABASE_COMMAND_TIMEOUT."""
        monkeypatch.setenv("DATABASE_CONNECT_TIMEOUT", "2.5")
        monkeypatch.setenv("DATABASE_COMMAND_TIMEOUT", "120")

        settings = DatabaseSettings()

        assert (settings.connect_timeout, settings.command_timeout) == (2.5, 120)

    @pytest.mark.parametrize("field", ["connect_timeout", "command_timeout"])
    def test_timeouts_must_be_positive(self, field):
        """[EC] 0 would make every connection or query fail at once."""
        with pytest.raises(pydantic.ValidationError, match=field):
            DatabaseSettings(**{field: 0})

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            # SQLAlchemy reads 0 as "no limit": 20 connections asked, 20 opened
            ("pool_size", 0),
            # ...and a negative size lowers the limit: -1 + 10 overflow = 9
            ("pool_size", -1),
            # -1 is SQLAlchemy's "no overflow limit"
            ("pool_max_overflow", -1),
            # A full pool would fail every request at once instead of waiting
            ("pool_timeout", 0),
            # Every checkout would open a new connection: no pool left
            ("pool_recycle", 0),
        ],
    )
    def test_pool_setting_out_of_range_refused(self, field, value):
        """[EC] A value SQLAlchemy reads in a surprising way -> refused at startup."""
        with pytest.raises(pydantic.ValidationError, match=field):
            DatabaseSettings(**{field: value})

    def test_smallest_pool_accepted(self):
        """[HP] One connection and no overflow is a valid, if small, pool."""
        settings = DatabaseSettings(pool_size=1, pool_max_overflow=0)

        assert (settings.pool_size, settings.pool_max_overflow) == (1, 0)


class TestEnvExample:
    """.env.example, which the README copies to .env to run the app on the host.

    WHY: nothing loaded it. A variable renamed in the code and not in the
    example would stop the first start of every new developer.
    """

    def test_is_a_valid_configuration(self, monkeypatch):
        """[HP] Every settings class starts from .env.example alone."""
        for cls in SETTINGS_CLASSES:
            monkeypatch.setitem(cls.model_config, "env_file", ENV_EXAMPLE)

        settings = Settings()

        # The example's value, not the default: the file was read
        assert settings.database.port == 5433

    def test_an_env_from_before_m10_still_starts(self, monkeypatch, tmp_path):
        """[EC] The KEYCLOAK_* and AUTH_COOKIE_* lines of an old .env are ignored.

        WHY: the login left in M10, and with it those settings. The .env of
        whoever runs the demo was copied from the .env.example of before:
        with a refusal of unknown names, the demo would not start.
        """
        old_lines = (
            "KEYCLOAK_HOST=localhost\n"
            "KEYCLOAK_PORT=8080\n"
            "KEYCLOAK_SCHEME=http\n"
            "KEYCLOAK_REALM=neuralbrewery\n"
            "KEYCLOAK_CLIENT_ID=neuralbrewery\n"
            "KEYCLOAK_CLIENT_SECRET=neuralbrewery-dev-secret\n"
            "KEYCLOAK_AUDIENCE=\n"
            "KEYCLOAK_REQUEST_TIMEOUT=10\n"
            "AUTH_COOKIE_SECURE=false\n"
            "AUTH_COOKIE_NAME=rt\n"
            "AUTH_COOKIE_SAMESITE=lax\n"
        )
        old_env = tmp_path / ".env"
        old_env.write_text(
            ENV_EXAMPLE.read_text(encoding="utf-8") + old_lines, encoding="utf-8"
        )
        for cls in SETTINGS_CLASSES:
            monkeypatch.setitem(cls.model_config, "env_file", old_env)

        settings = Settings()

        assert settings.database.port == 5433
        assert "keycloak" not in settings.model_dump()


class TestSecrets:
    """Database password, API keys of the two providers, approval token.

    WHY: settings reach logs and tracebacks through repr() and model_dump().
    As plain strings, both secrets were printed in full, and the password a
    second time inside the database URL.
    """

    @pytest.fixture
    def settings(self) -> Settings:
        return Settings(
            database=DatabaseSettings(password="db-secret-value"),
            claude=ClaudeSettings(api_key="sk-ant-secret-value"),
            openai_compat=OpenAICompatSettings(api_key="gm-secret-value"),
            approvals=ApprovalSettings(token="approval-secret-value"),
        )

    @pytest.mark.parametrize(
        "secret",
        [
            "db-secret-value",
            "sk-ant-secret-value",
            "gm-secret-value",
            "approval-secret-value",
        ],
    )
    def test_secret_not_in_repr_or_dumps(self, settings, secret):
        """[SEC] repr, model_dump and JSON of the whole settings hide it."""
        assert secret not in repr(settings)
        assert secret not in str(settings.model_dump())
        assert secret not in settings.model_dump_json()

    def test_secrets_readable_on_request(self, settings):
        """[HP] get_secret_value() gives the value to the code that needs it."""
        assert settings.database.password.get_secret_value() == "db-secret-value"
        assert settings.claude.api_key.get_secret_value() == "sk-ant-secret-value"
        assert settings.approvals.token.get_secret_value() == "approval-secret-value"


class TestErrorsShowNoValues:
    """A settings error at startup names the problem, not the values read.

    WHY: pydantic prints the input of a check that fails, and the input of a
    settings class holds the lines of .env it has no field for, secrets
    included. With DATABASE_PASSWORD on the last line of .env, the error of
    a rule on the cookie of the login showed the whole password; the
    production refusal, which promises no values, showed
    TEST_DATABASE_PASSWORD.
    """

    def test_server_error_shows_no_value(self, tmp_path):
        """[SEC] The refusal of a second worker, with a password last in .env."""
        env_file = tmp_path / ".env"
        env_file.write_text("SERVER_WORKERS=2\nDATABASE_PASSWORD=hunter2\n")

        with pytest.raises(pydantic.ValidationError) as exc_info:
            ServerSettings(_env_file=env_file)

        assert "hunter2" not in str(exc_info.value)

    def test_production_error_shows_no_value(
        self, production_env, monkeypatch, tmp_path
    ):
        """[SEC] The production refusal, with the test database's password in .env."""
        monkeypatch.setenv("APP_DEBUG", "true")
        env_file = tmp_path / ".env"
        env_file.write_text("TEST_DATABASE_PASSWORD=hunter2\n")

        with pytest.raises(pydantic.ValidationError) as exc_info:
            Settings(_env_file=env_file)

        assert "hunter2" not in str(exc_info.value)

    @pytest.mark.parametrize("cls", SETTINGS_CLASSES, ids=lambda cls: cls.__name__)
    def test_every_class_hides_its_input(self, cls):
        """[SEC] Every settings class keeps its input out of its errors."""
        assert cls.model_config.get("hide_input_in_errors") is True


class TestProductionChecks:
    """Outside development, development values stop the startup.

    WHY: the app started in production with debug on, the password
    "postgres" and the development trusted hosts. Staging then still started
    with all of them (tried on 3 November 2026). Each change below starts
    from a valid deploy (deployed),
    in staging and in production, and breaks one thing.
    """

    @pytest.fixture(params=["staging", "production"])
    def deployed(self, request, production_env, monkeypatch) -> dict[str, str]:
        """A valid deploy, in each environment the checks guard."""
        monkeypatch.setenv("APP_ENVIRONMENT", request.param)
        return {**production_env, "APP_ENVIRONMENT": request.param}

    def test_valid_deploy_starts(self, deployed):
        """[HP] Real values everywhere: no error."""
        assert Settings().app.environment == deployed["APP_ENVIRONMENT"]

    def test_development_defaults_still_start(self):
        """[HP] The checks never block development."""
        assert Settings().app.environment == "development"

    @pytest.mark.parametrize(
        ("change", "named"),
        [
            ({"APP_DEBUG": "true"}, "APP_DEBUG"),
            ({"DATABASE_PASSWORD": None}, "DATABASE_PASSWORD"),
            ({"DATABASE_PASSWORD": "appbase_secret_change_me"}, "DATABASE_PASSWORD"),
            # echo logs every query with its values: personal data in the logs
            ({"DATABASE_ECHO": "true"}, "DATABASE_ECHO"),
            ({"SERVER_CORS_ORIGINS": '["*"]'}, "SERVER_CORS_ORIGINS"),
            # Unset: the frontends of development, on localhost
            ({"SERVER_CORS_ORIGINS": None}, "SERVER_CORS_ORIGINS"),
            # A development origin left beside the real one
            (
                {
                    "SERVER_CORS_ORIGINS": (
                        '["https://app.example.com", "http://localhost:3000"]'
                    )
                },
                "SERVER_CORS_ORIGINS",
            ),
            (
                {"SERVER_CORS_ORIGINS": '["http://127.0.0.1:5173"]'},
                "SERVER_CORS_ORIGINS",
            ),
            ({"SERVER_TRUSTED_HOSTS": None}, "SERVER_TRUSTED_HOSTS"),
            ({"SERVER_TRUSTED_HOSTS": '["*"]'}, "SERVER_TRUSTED_HOSTS"),
            # Anyone could choose the client address the logs show
            ({"SERVER_FORWARDED_ALLOW_IPS": '["*"]'}, "SERVER_FORWARDED_ALLOW_IPS"),
            # Anyone could move the time of the plant and break it
            ({"PLANT_SIMULATION_CONTROL": "true"}, "PLANT_SIMULATION_CONTROL"),
            # Nobody could approve: the queue would only fill up
            ({"APPROVAL_TOKEN": None}, "APPROVAL_TOKEN"),
            ({"APPROVAL_TOKEN": "brewer-dev-token"}, "APPROVAL_TOKEN"),
        ],
        ids=[
            "debug",
            "db-password-default",
            "db-password-example",
            "db-echo",
            "cors-any-origin",
            "cors-unset",
            "cors-localhost-beside-the-frontend",
            "cors-loopback",
            "trusted-hosts-local",
            "trusted-hosts-any",
            "forwarded-any",
            "simulation-control",
            "approval-token-unset",
            "approval-token-example",
        ],
    )
    def test_development_value_refused(self, deployed, monkeypatch, change, named):
        """[SEC] One development value -> an error that names its variable."""
        for name, value in change.items():
            if value is None:
                monkeypatch.delenv(name)
            else:
                monkeypatch.setenv(name, value)

        with pytest.raises(pydantic.ValidationError) as exc_info:
            Settings()

        assert named in str(exc_info.value)

    def test_origin_named_like_localhost_accepted(self, deployed, monkeypatch):
        """[EC] Only the host localhost is local, not a name that contains it."""
        monkeypatch.setenv("SERVER_CORS_ORIGINS", '["https://localhost.example.com"]')

        assert Settings().server.cors_origins == ["https://localhost.example.com"]

    @pytest.mark.parametrize("environment", ["staging", "production"])
    def test_every_problem_in_one_error(self, monkeypatch, environment):
        """[HP] All development values at once -> one error listing them all.

        WHY: one error per restart would turn a deploy into a guessing game.
        """
        monkeypatch.setenv("APP_ENVIRONMENT", environment)
        monkeypatch.setenv("APP_DEBUG", "true")

        with pytest.raises(pydantic.ValidationError) as exc_info:
            Settings()

        message = str(exc_info.value)
        assert f"refusing to start in {environment}" in message
        for named in (
            "APP_DEBUG",
            "DATABASE_PASSWORD",
            "SERVER_CORS_ORIGINS",
            "SERVER_TRUSTED_HOSTS",
            "APPROVAL_TOKEN",
        ):
            assert named in message

    def test_error_shows_no_secret(self, deployed, monkeypatch):
        """[SEC] The error names variables, never their values."""
        monkeypatch.setenv("APP_DEBUG", "true")

        with pytest.raises(pydantic.ValidationError) as exc_info:
            Settings()

        assert deployed["DATABASE_PASSWORD"] not in str(exc_info.value)
        assert deployed["APPROVAL_TOKEN"] not in str(exc_info.value)


class TestServerSettings:
    """ServerSettings — server config and trusted hosts.

    WHY: trusted_hosts drives TrustedHostMiddleware. Wrong defaults
    mean the app rejects legitimate requests or accepts malicious ones.
    """

    def test_default_trusted_hosts(self):
        """[HP] Default trusted hosts include localhost for development."""
        settings = ServerSettings()
        assert "localhost" in settings.trusted_hosts
        assert "127.0.0.1" in settings.trusted_hosts

    def test_custom_trusted_hosts(self):
        """[HP] trusted_hosts can be overridden for production."""
        settings = ServerSettings(trusted_hosts=["myapp.example.com", "localhost"])
        assert settings.trusted_hosts == ["myapp.example.com", "localhost"]

    def test_default_cors_origins(self):
        """[HP] CORS origins default to common local dev ports."""
        settings = ServerSettings()
        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:5173" in settings.cors_origins

    def test_default_max_body_size(self):
        """[HP] Request bodies are limited to 64 KiB by default."""
        assert ServerSettings().max_body_size == 64 * 1024

    def test_max_body_size_must_be_positive(self):
        """[EC] 0 would answer 413 to every request with a body."""
        with pytest.raises(pydantic.ValidationError):
            ServerSettings(max_body_size=0)

    def test_default_graceful_shutdown_timeout(self):
        """[HP] Open requests get 5 seconds at shutdown, then uvicorn cancels them."""
        assert ServerSettings().timeout_graceful_shutdown == 5

    def test_graceful_shutdown_timeout_must_be_positive(self):
        """[EC] 0 or less would cut every open request at once."""
        with pytest.raises(pydantic.ValidationError):
            ServerSettings(timeout_graceful_shutdown=0)

    def test_one_worker_by_default(self):
        """[HP] One process: one plant."""
        assert ServerSettings().workers == 1

    @pytest.mark.parametrize("workers", [0, 2, 4])
    def test_any_other_number_of_workers_refused(self, workers, monkeypatch):
        """[EC] SERVER_WORKERS other than 1 stops the startup, in every environment.

        WHY: the plant lives in the process of the API. Two workers would
        hold two plants, each with its own time, and a command approved on
        one would never show on the other.
        """
        monkeypatch.setenv("SERVER_WORKERS", str(workers))

        with pytest.raises(pydantic.ValidationError, match="SERVER_WORKERS"):
            ServerSettings()

    def test_default_forwarded_allow_ips(self):
        """[HP] Only a proxy on the same host is trusted, as uvicorn does."""
        assert ServerSettings().forwarded_allow_ips == ["127.0.0.1"]

    def test_forwarded_allow_ips_from_env(self, monkeypatch):
        """[HP] A JSON list, like SERVER_TRUSTED_HOSTS; networks are accepted.

        WHY: uvicorn read FORWARDED_ALLOW_IPS from the environment of the
        process only, never from .env.
        """
        monkeypatch.setenv("SERVER_FORWARDED_ALLOW_IPS", '["172.18.0.0/16"]')

        assert ServerSettings().forwarded_allow_ips == ["172.18.0.0/16"]
