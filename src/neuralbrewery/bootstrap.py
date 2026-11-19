"""Composition root helpers — service initialization and shutdown.

start_services() is the one place that knows which services the app has:
another service changes this module, not main.py.

Every adapter goes into app.state through the StateKey of its port, next
to the getter that reads it (``PLANT_READER.set(state, ReadOnlyPlant(...))``):
mypy checks there that the adapter still matches the port.
"""

from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack
from functools import partial
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.transport_security import TransportSecuritySettings
from starlette.datastructures import State
from starlette.middleware.trustedhost import TrustedHostMiddleware

from neuralbrewery.adapters.claude import client as claude_adapter
from neuralbrewery.adapters.manuals.index import ManualIndex
from neuralbrewery.adapters.openai_compat import client as compat_adapter
from neuralbrewery.adapters.plant_sim.adapter import InProcessPlant
from neuralbrewery.adapters.plant_sim.simulator import PlantSimulator
from neuralbrewery.adapters.plant_sim.starts import brew_day, fermentation
from neuralbrewery.core.approvals.protocols import DecisionReader
from neuralbrewery.core.body_limit import BodySizeLimitMiddleware
from neuralbrewery.core.config import (
    DatabaseSettings,
    ManualsSettings,
    ServerSettings,
    Settings,
)
from neuralbrewery.core.database import DatabaseManager, database_url
from neuralbrewery.core.database.dependencies import DB_MANAGER
from neuralbrewery.core.error_middleware import UnhandledExceptionMiddleware
from neuralbrewery.core.logging import (
    REQUEST_ID_HEADER,
    LoggingMiddleware,
    get_logger,
)
from neuralbrewery.core.manuals.protocols import ManualSearch
from neuralbrewery.core.plant.dependencies import PLANT_READER
from neuralbrewery.core.plant.protocols import PlantReader
from neuralbrewery.core.plant.readonly import ReadOnlyPlant, SimulationOnly
from neuralbrewery.core.security import SecureHeadersMiddleware
from neuralbrewery.features.agents.mcp_server import MCP_SERVER, create_mcp_server
from neuralbrewery.features.agents.plant_agent import PlantAgent
from neuralbrewery.features.agents.router import (
    AGENT_SERVICE,
    PLANT_AGENT,
    PROPOSAL_INBOX,
)
from neuralbrewery.features.approvals.api.decisions import QueueDecisions
from neuralbrewery.features.approvals.api.executor import EXECUTOR, Executor
from neuralbrewery.features.approvals.api.inbox import QueueInbox, database_log
from neuralbrewery.features.health.router import health_router
from neuralbrewery.features.plant.router import SIMULATION_CONTROL

logger = get_logger(__name__)

CleanupFn = Callable[[], Awaitable[Any]]

STARTS: dict[str, Callable[..., PlantSimulator]] = {
    "brew_day": brew_day,
    "fermentation": fermentation,
}


MCP_PATH = "/mcp"


def init_plant(app: FastAPI, settings: Settings) -> None:
    """The simulated plant in this process, each consumer with its own port.

    Until M2 the plant lives here, built from a named start and its seed.
    The plant keeps that start, so POST /simulation/restart builds a new
    one inside the same object, as a restart of the container would. The
    in-process adapter implements the three ports in one object, so nobody
    gets it as it is: readers a ReadOnlyPlant, the executor alone the
    buttons, and the routes of the simulation a SimulationOnly, only when
    PLANT_SIMULATION_CONTROL is on. Nothing runs in the background: time
    moves only through those routes.

    The MCP server gets the reader and the inbox of proposals, never the
    executor. The MCP server answers at /mcp, and start_services() runs
    it. The plant agent gets the reader and the decisions of the brewer
    on its past proposals, read from the same queue: its memory. Its
    proposals reach the inbox through its endpoint. It exists only with
    the key of its provider (init_plant_agent).
    """
    plant_settings = settings.plant
    start = partial(STARTS[plant_settings.start], seed=plant_settings.seed)
    plant = InProcessPlant(start(), start=start)
    reader = ReadOnlyPlant(plant)
    PLANT_READER.set(app.state, reader)
    EXECUTOR.set(app.state, Executor(plant))
    if plant_settings.simulation_control:
        SIMULATION_CONTROL.set(app.state, SimulationOnly(plant))

    log = database_log(lambda: DB_MANAGER.get(app.state))
    inbox = QueueInbox(log, reader)
    PROPOSAL_INBOX.set(app.state, inbox)
    init_plant_agent(app, settings, reader, QueueDecisions(log))

    server = create_mcp_server(reader, inbox)
    MCP_SERVER.set(app.state, server)
    # Stateless, one JSON answer per request: no session to keep between
    # calls. Its route joins the app's, behind the same middleware.
    mcp_http = server.streamable_http_app(
        streamable_http_path=MCP_PATH,
        stateless_http=True,
        json_response=True,
        transport_security=mcp_transport_security(settings.server),
    )
    app.router.routes.extend(mcp_http.routes)


def agent_key(settings: Settings) -> str:
    """The key of the provider the agents run on: the other one does not count."""
    if settings.agent.provider == "openai_compat":
        return settings.openai_compat.api_key.get_secret_value()
    return settings.claude.api_key.get_secret_value()


def manual_search(settings: ManualsSettings) -> ManualSearch | None:
    """The search over the manuals, read once now; None when it is off.

    On, ManualsSettings has already checked that the folder holds the text.
    """
    if not settings.enabled:
        return None
    return ManualIndex.from_folder(settings.folder)


def init_plant_agent(
    app: FastAPI, settings: Settings, reader: PlantReader, decisions: DecisionReader
) -> None:
    """The plant agent on the provider of AGENT_PROVIDER: it reads, and recalls.

    Of the plant it gets the reader alone, of the queue the brewer's
    decisions on its past proposals: nothing that proposes or approves.
    With MANUALS_ENABLED it gets the search over the manuals too: text, and
    nothing more.

    The agent takes a datapizza client and the arguments of every call, and
    knows no more of its provider. Without the key of that provider there
    is no agent, and its endpoint answers 503 naming the provider.
    """
    if settings.agent.provider == "openai_compat":
        AGENT_SERVICE.set(app.state, compat_adapter.SERVICE)
        if agent_key(settings):
            agent = PlantAgent(
                reader,
                decisions,
                compat_adapter.create_client(settings.openai_compat),
                compat_adapter.generation_args(),
                manuals=manual_search(settings.manuals),
            )
            PLANT_AGENT.set(app.state, agent)
        return
    AGENT_SERVICE.set(app.state, claude_adapter.SERVICE)
    if agent_key(settings):
        agent = PlantAgent(
            reader,
            decisions,
            claude_adapter.create_client(settings.claude),
            claude_adapter.generation_args(settings.claude),
            manuals=manual_search(settings.manuals),
        )
        PLANT_AGENT.set(app.state, agent)


def mcp_transport_security(settings: ServerSettings) -> TransportSecuritySettings:
    """The MCP server's own check of Host and Origin, on the app's lists.

    Left to itself it allows only 127.0.0.1 and localhost with a port: the
    test client's Host, or a domain in SERVER_TRUSTED_HOSTS, would get 421.
    With "*" (development only) TrustedHostMiddleware takes any Host, and
    so does this.
    """
    if "*" in settings.trusted_hosts:
        return TransportSecuritySettings(enable_dns_rebinding_protection=False)
    return TransportSecuritySettings(
        allowed_hosts=[
            name for host in settings.trusted_hosts for name in (host, f"{host}:*")
        ],
        allowed_origins=settings.cors_origins,
    )


def _log_start_failure(event: str, error: Exception) -> None:
    """One error line for a service that does not start.

    No traceback: uvicorn prints it when the startup fails. The line names
    the cause of a wrapped error, as the readiness log does.
    """
    cause = error.__cause__ or error
    logger.error(event, error_type=type(cause).__name__, error=str(cause))


async def start_services(
    app_state: State, settings: Settings, services: list[tuple[str, CleanupFn]]
) -> None:
    """Open every service, and put each adapter in app state.

    Each service goes into ``services`` as soon as it is open, so the
    caller can close it whatever happens next: a later service that fails
    to start, or a cancellation.
    """
    # Built by create_app, which logs nothing: said here, as the app starts
    logger.info(
        "plant_ready",
        start=settings.plant.start,
        seed=settings.plant.seed,
        simulation_control=settings.plant.simulation_control,
        # Without the key of its provider the agent endpoint answers 503
        agent_provider=settings.agent.provider,
        agent=bool(agent_key(settings)),
        manuals=settings.manuals.enabled,
    )
    db_manager = await init_database(app_state, settings.database)
    services.append(("database", db_manager.disconnect))

    # Last: the MCP server answers once what it reaches is open
    await start_mcp_server(app_state, services)


async def start_mcp_server(
    app_state: State, services: list[tuple[str, CleanupFn]]
) -> None:
    """Run the session manager of the MCP server until the app stops."""
    stack = AsyncExitStack()
    await stack.enter_async_context(MCP_SERVER.get(app_state).session_manager.run())
    services.append(("mcp_server", stack.aclose))


async def init_database(
    app_state: State, settings: DatabaseSettings
) -> DatabaseManager:
    """Create connection pool, verify connectivity, register in app state."""
    db_manager = DatabaseManager(settings)
    await db_manager.connect()

    try:
        await db_manager.health_check()
    except Exception as e:
        _log_start_failure("database_connection_failed", e)
        await db_manager.disconnect()
        raise

    logger.info(
        "database_connected",
        url=database_url(settings).render_as_string(hide_password=True),
    )
    # app.state holds the port, for the routes. The lifespan gets the
    # manager itself, because disconnect() is not part of the port.
    DB_MANAGER.set(app_state, db_manager)
    return db_manager


async def shutdown_services(
    services: list[tuple[str, CleanupFn]],
) -> None:
    """Graceful shutdown in reverse initialization order."""
    for name, close in reversed(services):
        try:
            await close()
        except Exception:
            logger.exception("shutdown_failed", service=name)


def register_middleware(app: FastAPI, settings: ServerSettings) -> None:
    """Register middleware. ORDER MATTERS: execute in REVERSE add order.

    A request crosses them from the last added to the first, then reaches
    the routes; the response goes back the other way:
    Logging → TrustedHost → SecureHeaders → CORS → BodySizeLimit →
    UnhandledException → routes.
    """
    # Closest to the routes: an unexpected exception becomes a 500 here, and
    # on its way out the 500 gets CORS, security headers and X-Request-ID
    # like any other response.
    app.add_middleware(UnhandledExceptionMiddleware)

    # Inside CORS, so its 413 gets the same headers as any other error.
    app.add_middleware(BodySizeLimitMiddleware, max_body_size=settings.max_body_size)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
        # The browser hides from JavaScript the headers CORS does not
        # expose: without this a frontend cannot show the request id of
        # a failed request, or read when to retry a 503.
        expose_headers=[REQUEST_ID_HEADER, "Retry-After"],
    )

    app.add_middleware(SecureHeadersMiddleware)

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.trusted_hosts,
    )

    # Outermost: sees every request first and every response last. Docker's
    # HEALTHCHECK and the orchestrator call the health probes all day:
    # their request lines go to DEBUG.
    app.add_middleware(LoggingMiddleware, quiet_prefixes=[health_router.prefix])
