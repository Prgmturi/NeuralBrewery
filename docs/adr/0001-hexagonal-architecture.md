# 0001. Ports in core, adapters in adapters/, wired in bootstrap.py

Status: accepted. Recorded on 27 October 2026. Examples updated on 17 November 2026 (M10), when the login of the template and its Keycloak adapters left the project.

## Context

The project is a template that teaches: whoever starts from it should find the business rules apart from the libraries and services they use, and be able to test the rules without them.

## Decision

- **Ports** are `Protocol` classes: `core/plant/protocols.py` (`PlantReader`, `PlantCommander`, `SimulationControl`), `core/approvals/protocols.py`, `core/manuals/protocols.py`, `core/protocols.py` (`HealthCheckable`), `core/database/protocols.py` (`DatabaseProvider`), and the ports of a feature's own domain, such as `features/approvals/domain/protocols.py`.
- **Adapters** implement them, one folder per external service: `adapters/plant_sim/` is the simulated plant, `adapters/claude/` and `adapters/openai_compat/` the clients of the two model providers, `adapters/manuals/` the search over the manuals.
- **`bootstrap.py`** is the only module that builds the adapters and hands them to the app. It stores each one in `app.state` through the `StateKey` of its port (`core/state.py`), so mypy checks that an adapter still matches its port.
- **The rules are checked on every push:** import contracts in `pyproject.toml` (layers, ports that import no adapter, a domain that imports no framework), plus tests that import modules in a new process, to see what an `__init__.py` pulls in.

## Consequences

- The domain of a feature and the watcher are tested with fakes, in milliseconds.
- Another service means another folder in `adapters/`, its settings in `core/config/` and its wiring in `bootstrap.py`: a real controller instead of the simulated plant changes only the adapter.
- Settings stay in `core/config/`: `Settings` gathers every section there, and `core` never imports an adapter.
- More files than a flat project, and a rule to learn: a module imports only from the layers below its own.
