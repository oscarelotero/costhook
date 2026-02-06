"""enable_rls_on_alembic_version

Revision ID: abdbdc42036f
Revises: 59dc34194f36
Create Date: 2026-02-05 19:41:08.441645

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abdbdc42036f'
down_revision: str | None = '59dc34194f36'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE public.alembic_version ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.execute("ALTER TABLE public.alembic_version DISABLE ROW LEVEL SECURITY")
