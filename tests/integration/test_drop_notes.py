"""The migration that drops the table of the notes, on a real Postgres.

Module under test: alembic/versions/3f1c9a7d2e64_drop_notes_table.py
Layer: Migrations, real database

WHY: the notes were the CRUD example of the template, gone in M10. A
database made before then has their table, the demo's included: the
migration drops it only while it is empty, so that no row is lost without
a word. Downgrade gives the table back, empty.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import text

from tests.integration.settings import IntegrationDatabaseSettings

REPOSITORY = Path(__file__).parent.parent.parent
# The migration before the drop: the table of the notes is there
BEFORE_THE_DROP = "00b0ef650519"


def alembic(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Alembic on the test database, from a folder without .env."""
    database = IntegrationDatabaseSettings()
    return subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(REPOSITORY / "alembic.ini")]
        + list(args),
        cwd=tmp_path,
        env={
            **os.environ,
            "DATABASE_HOST": database.host,
            "DATABASE_PORT": str(database.port),
            "DATABASE_NAME": database.name,
            "DATABASE_USER": database.user,
            "DATABASE_PASSWORD": database.password.get_secret_value(),
        },
        capture_output=True,
        text=True,
        check=False,
    )


async def tables(db_manager) -> set[str]:
    async with db_manager.engine.connect() as connection:
        result = await connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        return {row[0] for row in result}


@pytest.fixture
def before_the_drop(migrated_database, tmp_path):
    """The database one migration back, with its table of notes; head after."""
    downgrade = alembic(tmp_path, "downgrade", BEFORE_THE_DROP)
    assert downgrade.returncode == 0, downgrade.stderr
    yield
    upgrade = alembic(tmp_path, "upgrade", "head")
    assert upgrade.returncode == 0, upgrade.stderr


async def test_drops_the_empty_table(before_the_drop, db_manager, tmp_path):
    """[HP] An empty table of notes goes; the audit of the approvals stays."""
    assert "notes" in await tables(db_manager)

    result = alembic(tmp_path, "upgrade", "head")

    assert result.returncode == 0, result.stderr
    assert "notes" not in await tables(db_manager)
    assert "approval_events" in await tables(db_manager)


async def test_stops_on_a_table_with_rows(before_the_drop, db_manager, tmp_path):
    """[SEC] A note in the table: the migration stops, and the note stays."""
    async with db_manager.engine.begin() as connection:
        await connection.execute(
            text(
                "INSERT INTO notes (id, owner_id, title, body, created_at, updated_at)"
                " VALUES (gen_random_uuid(), 'brewer', 'kept', '', now(), now())"
            )
        )

    result = alembic(tmp_path, "upgrade", "head")

    assert result.returncode != 0
    assert "notes holds rows" in result.stderr
    async with db_manager.engine.begin() as connection:
        count = await connection.scalar(text("SELECT count(*) FROM notes"))
        await connection.execute(text("DELETE FROM notes"))
    assert count == 1
