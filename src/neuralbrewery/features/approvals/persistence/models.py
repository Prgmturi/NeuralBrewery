from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from neuralbrewery.core.database import Base
from neuralbrewery.features.approvals.domain.proposal import BY_MAX_LENGTH, STEPS


def _kind_matches_seq() -> str:
    """The SQL of the rule: the seq of an event is its step."""
    steps = [
        f"(seq = {seq} AND kind IN ({', '.join(f"'{kind}'" for kind in sorted(step))}))"
        for seq, step in enumerate(STEPS)
    ]
    return " OR ".join(steps)


class ApprovalEventRow(Base):
    """The table of the audit: an event per step of each proposal.

    Rows are only added. The migration adds a trigger that refuses UPDATE,
    DELETE and TRUNCATE, for the owner of the table too. The unique
    (proposal_id, seq) and the check of the kind give each proposal one
    birth, one decision and one outcome: of two approvals at once, the
    second fails here, before its button is pressed.
    """

    __tablename__ = "approval_events"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    # Indexed by the unique (proposal_id, seq), whose first column it is
    proposal_id: Mapped[UUID]
    seq: Mapped[int]
    kind: Mapped[str] = mapped_column(String(32))
    actor: Mapped[str] = mapped_column(String(16))
    # The name of who acted, as declared: nobody checks it
    actor_name: Mapped[str] = mapped_column(String(BY_MAX_LENGTH))
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)
    sim_time_s: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("proposal_id", "seq"),
        CheckConstraint(_kind_matches_seq(), name="kind_matches_seq"),
    )
