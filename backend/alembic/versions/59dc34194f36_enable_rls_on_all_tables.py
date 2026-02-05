"""enable rls on all tables

Revision ID: 59dc34194f36
Revises: 062c1d0b55e2
Create Date: 2026-02-05 16:13:27.837561

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59dc34194f36'
down_revision: str | None = '062c1d0b55e2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE providers ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE cost_records ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    op.execute("ALTER TABLE cost_records DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE providers DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE user_profiles DISABLE ROW LEVEL SECURITY")
