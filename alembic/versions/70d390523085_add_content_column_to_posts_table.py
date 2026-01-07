"""add content column to posts table

Revision ID: 70d390523085
Revises: 5ccebb47cfff
Create Date: 2026-01-07 22:45:05.550373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '70d390523085'
down_revision: Union[str, Sequence[str], None] = '5ccebb47cfff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","content")
