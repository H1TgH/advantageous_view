"""add speed_weight to preferences

Revision ID: 0007
Revises: 0006
Create Date: 2026-05-23 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0007"
down_revision: Union[str, Sequence[str], None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_preferences",
        sa.Column("speed_weight", sa.Float(), server_default="0.2", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("user_preferences", "speed_weight")
