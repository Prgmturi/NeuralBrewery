"""Tests for bootstrap.py — composition root service initialization.

Module under test: src/neuralbrewery/bootstrap.py
Layer: Application integration (composition root)

WHY these tests exist: bootstrap.py wires all the concrete implementations
together. It is the only place where concrete classes appear. We verify
the wiring and error handling — particularly that partial initialization
failures properly clean up already-initialized resources.
"""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import State
from starlette.middleware.trustedhost import TrustedHostMiddleware

from neuralbrewery.bootstrap import (
    init_database,
    mcp_transport_security,
    register_middleware,
    shutdown_services,
)
from neuralbrewery.core.body_limit import BodySizeLimitMiddleware
from neuralbrewery.core.config import DatabaseSettings, ServerSettings
from neuralbrewery.core.database import DatabaseManager
from neuralbrewery.core.error_middleware import UnhandledExceptionMiddleware
from neuralbrewery.core.exceptions import ServiceUnavailableError
from neuralbrewery.core.logging import LoggingMiddleware
from neuralbrewery.core.security import SecureHeadersMiddleware
from neuralbrewery.main import create_app, lifespan


@pytest.fixture
async def http_client():
    """Real client, never used for requests: only passed around and inspected."""
    async with httpx.AsyncClient() as client:
        yield client


class TestInitDatabase:
    """init_database() — database initialization.

    WHY: Called at startup. If it fails, the app must not start
    with a half-initialized database connection.
    """

    @patch("neuralbrewery.bootstrap.DatabaseManager")
    async def test_creates_manager_and_connects(self, mock_database_manager):
        """[HP] Creates DatabaseManager, calls connect(), stores in state."""
        mock_manager = AsyncMock()
        mock_manager.connect = AsyncMock()
        mock_manager.health_check = AsyncMock(return_value=True)
        mock_database_manager.return_value = mock_manager

        state = State()
        settings = DatabaseSettings()
        result = await init_database(state, settings)

        mock_manager.connect.assert_called_once()
        mock_manager.health_check.assert_called_once()
        assert state.db_manager is mock_manager
        assert result is mock_manager

    @patch("neuralbrewery.bootstrap.DatabaseManager")
    async def test_health_check_failure_disconnects_and_raises(
        self, mock_database_manager
    ):
        """[EC] health_check fails -> disconnect called, exception propagates.

        WHY: Ensures no resource leak if DB is unreachable at startup.
        """
        mock_manager = AsyncMock()
        mock_manager.connect = AsyncMock()
        mock_manager.health_check = AsyncMock(side_effect=RuntimeError("DB down"))
        mock_manager.disconnect = AsyncMock()
        mock_database_manager.return_value = mock_manager

        state = State()
        settings = DatabaseSettings()
        with pytest.raises(RuntimeError, match="DB down"):
            await init_database(state, settings)

        mock_manager.disconnect.assert_called_once()

    @patch("neuralbrewery.bootstrap.DatabaseManager")
    async def test_failure_logs_the_cause_without_traceback(
        self, mock_database_manager, monkeypatch
    ):
        """[EC] One error line, naming the cause of the 503.

        WHY: logger.exception printed the traceback, and uvicorn printed it
        again when the startup failed: 336 lines with Postgres down (tried
        on 3 November 2026). uvicorn still prints it once.
        """
        logger = MagicMock()
        monkeypatch.setattr("neuralbrewery.bootstrap.logger", logger)
        unavailable = ServiceUnavailableError("database", retry_after=5)
        unavailable.__cause__ = ConnectionRefusedError(111, "Connection refused")
        mock_manager = AsyncMock()
        mock_manager.health_check = AsyncMock(side_effect=unavailable)
        mock_database_manager.return_value = mock_manager

        with pytest.raises(ServiceUnavailableError):
            await init_database(State(), DatabaseSettings())

        logger.error.assert_called_once_with(
            "database_connection_failed",
            error_type="ConnectionRefusedError",
            error="[Errno 111] Connection refused",
        )
        logger.exception.assert_not_called()

    @patch("neuralbrewery.bootstrap.DatabaseManager")
    async def test_logs_the_url_without_the_password(
        self, mock_database_manager, monkeypatch
    ):
        """[SEC] database_connected names the database, hides the password.

        WHY a fake logger: module loggers are cached on first use
        (cache_logger_on_first_use), so capture_logs cannot see them.
        """
        mock_database_manager.return_value = AsyncMock()
        logger = MagicMock()
        monkeypatch.setattr("neuralbrewery.bootstrap.logger", logger)

        await init_database(State(), DatabaseSettings(password="db-secret-value"))

        logger.info.assert_called_once_with(
            "database_connected",
            url="postgresql+asyncpg://postgres:***@localhost:5432/appbase",
        )


class OfflineDatabaseManager(DatabaseManager):
    """The real manager, minus the one query that needs a server.

    connect() builds the engine without connecting: SQLAlchemy opens the
    first connection at the first query, and health_check runs that query.
    """

    async def health_check(self) -> bool:
        return True


class TestServicesReachTheRoutes:
    """What bootstrap.py stores in app.state is what the routes receive.

    WHY: bootstrap.py stores each service in app.state under a name, and a
    getter (get_db_manager) reads it back by the same name. app.state has
    no types, and the other tests replace the getters: with a misspelled
    name mypy and every test passed, while in production each route that
    needs the service answered 500. Here the real lifespan runs with only
    the database replaced, and the routes get their real dependencies.
    """

    @pytest.fixture
    async def started_client(
        self, settings, monkeypatch
    ) -> AsyncGenerator[httpx.AsyncClient]:
        """Client for the app after its real startup, with no database."""
        monkeypatch.setattr(
            "neuralbrewery.bootstrap.DatabaseManager", OfflineDatabaseManager
        )
        app = create_app(settings)

        async with (
            lifespan(app),
            httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://testserver"
            ) as client,
        ):
            yield client

    async def test_readiness_gets_the_database(self, started_client):
        """[HP] get_db_manager finds what bootstrap.py stored."""
        response = await started_client.get("/health/ready")

        assert response.status_code == 200
        assert response.json()["checks"] == {"database": {"status": "healthy"}}


class TestShutdownServices:
    """shutdown_services() — graceful shutdown.

    WHY: Must call all cleanup functions even if some fail.
    Reverse order ensures dependencies are cleaned up last.
    """

    async def test_calls_all_cleanup_functions(self):
        """[HP] All registered cleanup functions called."""
        fn1 = AsyncMock()
        fn2 = AsyncMock()
        fn3 = AsyncMock()

        await shutdown_services([("svc1", fn1), ("svc2", fn2), ("svc3", fn3)])

        fn1.assert_called_once()
        fn2.assert_called_once()
        fn3.assert_called_once()

    async def test_reverse_order(self):
        """[HP] Cleanup functions called in reverse registration order.

        WHY: Services initialized first may depend on services initialized
        later. Reverse order ensures dependents are shut down first.
        """
        call_order: list[str] = []

        async def fn_a():
            call_order.append("a")

        async def fn_b():
            call_order.append("b")

        async def fn_c():
            call_order.append("c")

        await shutdown_services([("a", fn_a), ("b", fn_b), ("c", fn_c)])

        assert call_order == ["c", "b", "a"]

    async def test_continues_on_failure(self):
        """[EC] One cleanup function raises -> others still called.

        WHY: shutdown must be robust. A failing service should not
        prevent other services from shutting down cleanly.
        """
        fn1 = AsyncMock()
        fn2 = AsyncMock(side_effect=RuntimeError("failed"))
        fn3 = AsyncMock()

        # Should not raise despite fn2 failing
        await shutdown_services([("svc1", fn1), ("svc2", fn2), ("svc3", fn3)])

        # fn3 called first (reversed), then fn2 (fails), then fn1 (still called)
        fn1.assert_called_once()
        fn3.assert_called_once()

    async def test_empty_services_list(self):
        """[EC] Empty list -> no errors, no calls."""
        await shutdown_services([])  # Should not raise


class TestRegisterMiddleware:
    """register_middleware() — the order the middleware runs in.

    WHY: a response gets a middleware's headers only if it passes through
    that middleware. The error middleware must be the closest to the
    routes, or its 500 skips the others.
    """

    def test_error_middleware_is_closest_to_the_routes(self):
        """[HP] From outermost to innermost, as the docstring says."""
        app = FastAPI()

        register_middleware(app, ServerSettings())

        assert [middleware.cls for middleware in app.user_middleware] == [
            LoggingMiddleware,
            TrustedHostMiddleware,
            SecureHeadersMiddleware,
            CORSMiddleware,
            BodySizeLimitMiddleware,
            UnhandledExceptionMiddleware,
        ]


class TestMcpTransportSecurity:
    """The MCP server's own check of Host and Origin, on the app's lists.

    WHY: left to its default, the MCP server allows only 127.0.0.1 and
    localhost with a port. The test client's Host "testserver", or the
    domain of a deploy, got 421 Misdirected Request (tried on 15 November
    2026, at the probe of M4).
    """

    def test_every_trusted_host_with_any_port(self):
        """[HP] The hosts of SERVER_TRUSTED_HOSTS, alone and with a port."""
        security = mcp_transport_security(
            ServerSettings(
                trusted_hosts=["api.example.com"],
                cors_origins=["https://app.example.com"],
            )
        )

        assert security.enable_dns_rebinding_protection
        assert security.allowed_hosts == ["api.example.com", "api.example.com:*"]
        assert security.allowed_origins == ["https://app.example.com"]

    def test_any_host_switches_the_check_off(self):
        """[EC] "*" in development: TrustedHost takes any Host, and so does MCP."""
        security = mcp_transport_security(ServerSettings(trusted_hosts=["*"]))

        assert not security.enable_dns_rebinding_protection
