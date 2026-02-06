"""add_indexes_on_foreign_keys

Revision ID: d46d9a347500
Revises: abdbdc42036f
Create Date: 2026-02-05 19:43:59.138825

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd46d9a347500'
down_revision: str | None = 'abdbdc42036f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index("ix_providers_user_id", "providers", ["user_id"])
    op.create_index("ix_cost_records_provider_id", "cost_records", ["provider_id"])


def downgrade() -> None:
    op.drop_index("ix_cost_records_provider_id", table_name="cost_records")
    op.drop_index("ix_providers_user_id", table_name="providers")
