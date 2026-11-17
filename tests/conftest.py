"""
Root conftest — global fixtures available to all tests.

Fixture hierarchy:
    tests/conftest.py           ← YOU ARE HERE (isolation, settings, app, client)
    tests/core/database/conftest.py ← db-specific (mock session, mock manager)
    tests/features/conftest.py  ← feature-level (dependency overrides)
"""

import os
from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic_settings import BaseSettings

from neuralbrewery.core.config import ServerSettings, Settings, get_settings
from neuralbrewery.core.database.dependencies import get_db_manager
from neuralbrewery.main import create_app

# ---------------------------------------------------------------------------
# Isolation from the machine running the tests
# ---------------------------------------------------------------------------

# Settings plus the sections it nests (AppSettings, DatabaseSettings, ...),
# taken from its fields: a new section is isolated without touching this file.
SETTINGS_CLASSES: tuple[type[BaseSettings], ...] = (
    Settings,
    *(field.annotation for field in Settings.model_fields.values()),
)


def variable_name(cls: type[BaseSettings], field: str) -> str:
    """The variable pydantic-settings reads for a field.

    The prefix plus the field name, or the alias when the field has one.
    """
    alias = cls.model_fields[field].validation_alias
    if isinstance(alias, str):
        return alias.upper()
    return f"{cls.model_config.get('env_prefix', '')}{field}".upper()


@pytest.fixture(autouse=True)
def hermetic_settings(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Make every test independent of the machine that runs it.

    WHY: settings classes read the local .env and exported variables
    (APP_ENVIRONMENT, DATABASE_*, ...). With them, the same test passes on
    one machine and fails on another. Here both sources are switched off:
    a settings object built in a test holds the code defaults plus what
    the test passes explicitly.
    """
    for cls in SETTINGS_CLASSES:
        # pydantic-settings reads model_config["env_file"] at every
        # instantiation, so this applies to objects built during the test.
        monkeypatch.setitem(cls.model_config, "env_file", None)

        # Remove exactly the variables this class would read.
        names = {variable_name(cls, field) for field in cls.model_fields}
        for variable in list(os.environ):
            if variable.upper() in names:
                monkeypatch.delenv(variable)

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


# A production deploy that passes the production checks (Settings refuses
# development values when APP_ENVIRONMENT=production).
PRODUCTION_ENV = {
    "APP_ENVIRONMENT": "production",
    "DATABASE_PASSWORD": "db-password-from-the-vault",
    "SERVER_CORS_ORIGINS": '["https://app.example.com"]',
    "SERVER_TRUSTED_HOSTS": '["api.example.com"]',
    "APPROVAL_TOKEN": "approval-token-from-the-vault",
}


@pytest.fixture
def production_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Export PRODUCTION_ENV, as a real deploy would.

    Runs after hermetic_settings (autouse fixtures come first), so these
    are the only variables the settings see.
    """
    for name, value in PRODUCTION_ENV.items():
        monkeypatch.setenv(name, value)
    return PRODUCTION_ENV


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------


@asynccontextmanager
async def _noop_lifespan(app):
    """Lifespan that skips all service initialization."""
    yield


@pytest.fixture
def settings() -> Settings:
    """Settings for the test app: code defaults plus the test host.

    httpx sends ``Host: testserver``; TrustedHostMiddleware answers 400
    to any host missing from trusted_hosts.
    """
    return Settings(
        server=ServerSettings(trusted_hosts=["testserver", "localhost", "127.0.0.1"]),
    )


@pytest.fixture
def app(settings, mock_db_provider):
    """FastAPI app with external dependencies replaced by mocks."""
    application = create_app(settings)

    # Skip the real lifespan (no DB)
    application.router.lifespan_context = _noop_lifespan
    application.dependency_overrides[get_db_manager] = lambda: mock_db_provider
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
async def client(app) -> AsyncGenerator[AsyncClient]:
    """Async HTTP client for endpoint testing."""
    async with AsyncClient(
        transport=ASGITransport(app=app, raise_app_exceptions=False),
        base_url="http://testserver",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Mock services
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_db_provider():
    """AsyncMock implementing DatabaseProvider / HealthCheckable."""
    mock = AsyncMock()
    mock.health_check = AsyncMock(return_value=True)
    return mock
