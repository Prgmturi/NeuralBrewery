"""drop notes table

Revision ID: 3f1c9a7d2e64
Revises: 00b0ef650519
Create Date: 2026-11-17 18:00:00.000000

The notes were the CRUD example of the template, gone in M10. The table is
dropped only while it is empty: with a row in it the migration stops, and
nothing is lost (tests/integration/test_drop_notes.py). The check is SQL,
so it also holds in the script that --sql writes. Downgrade gives the table
back as the first migration made it, empty.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f1c9a7d2e64"
down_revision: str | Sequence[str] | None = "00b0ef650519"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ONLY_IF_EMPTY = """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM notes) THEN
        RAISE EXCEPTION 'notes holds rows: save or delete them, then migrate again';
    END IF;
END
$$
"""


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(ONLY_IF_EMPTY)
    op.drop_index(op.f("ix_notes_owner_id"), table_name="notes")
    op.drop_table("notes")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "notes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("owner_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notes")),
    )
    op.create_index(op.f("ix_notes_owner_id"), "notes", ["owner_id"], unique=False)
