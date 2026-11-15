"""create approval events table

Revision ID: 00b0ef650519
Revises: badd4ec74942
Create Date: 2026-11-15 02:13:14.069480

The audit of the approvals. Rows are only added: a trigger refuses UPDATE,
DELETE and TRUNCATE. A REVOKE would not do, because the app connects as the
owner of the table, and an owner keeps its rights. Downgrade still drops
the table: that is a migration, not the app.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "00b0ef650519"
down_revision: str | Sequence[str] | None = "badd4ec74942"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

APPEND_ONLY = """
CREATE FUNCTION approval_events_append_only() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'approval_events: rows are only added, % refused', TG_OP;
END
$$
"""


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "approval_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("proposal_id", sa.Uuid(), nullable=False),
        sa.Column("seq", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("actor", sa.String(length=16), nullable=False),
        sa.Column("actor_name", sa.String(length=100), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("sim_time_s", sa.Double(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "(seq = 0 AND kind IN ('blocked', 'proposed')) "
            "OR (seq = 1 AND kind IN ('approved', 'rejected')) "
            "OR (seq = 2 AND kind IN ('executed', 'execution_failed'))",
            name=op.f("ck_approval_events_kind_matches_seq"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_approval_events")),
        sa.UniqueConstraint(
            "proposal_id", "seq", name=op.f("uq_approval_events_proposal_id_seq")
        ),
    )
    op.execute(APPEND_ONLY)
    op.execute(
        "CREATE TRIGGER approval_events_no_change BEFORE UPDATE OR DELETE "
        "ON approval_events FOR EACH ROW "
        "EXECUTE FUNCTION approval_events_append_only()"
    )
    op.execute(
        "CREATE TRIGGER approval_events_no_truncate BEFORE TRUNCATE "
        "ON approval_events FOR EACH STATEMENT "
        "EXECUTE FUNCTION approval_events_append_only()"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("approval_events")  # its triggers go with it
    op.execute("DROP FUNCTION approval_events_append_only()")
