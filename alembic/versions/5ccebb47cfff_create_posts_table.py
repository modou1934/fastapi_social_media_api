"""create_posts_table

Revision ID: 5ccebb47cfff
Revises: 
Create Date: 2026-01-07 22:34:50.390397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = '5ccebb47cfff'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True,nullable=False),
        sa.Column("title", sa.String(), nullable=False),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
