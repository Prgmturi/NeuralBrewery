# Architecture decision records

Short notes on the decisions that shape the project: the context, the decision, and what follows from it. A record is not rewritten when a decision changes: a new one replaces it, and says which. These are the decisions of the template the project grew from; those of the project are in [decisioni.md](../decisioni.md). 0002 (Keycloak) and 0003 (the refresh token in a cookie) left with the login, in M10: they stay in the history of git.

| Record | Decision |
|---|---|
| [0001](0001-hexagonal-architecture.md) | Ports in `core`, adapters in `adapters/`, wired in `bootstrap.py` |
| [0004](0004-app-factory.md) | The app is built by a factory, `create_app()` |
| [0005](0005-database.md) | SQLAlchemy is part of `core`; a feature with rules keeps it behind a port |
| [0006](0006-errors.md) | One format for errors, and adapters translate the errors of their libraries |
| [0007](0007-development-values.md) | Staging and production refuse to start on a development value |
