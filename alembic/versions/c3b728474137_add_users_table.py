"""add users table

Revision ID: c3b728474137
Revises: 70d390523085
Create Date: 2026-01-07 22:51:39.041664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  


# revision identifiers, used by Alembic.
revision: str = 'c3b728474137'
down_revision: Union[str, Sequence[str], None] = '70d390523085'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
    sa.Column("id",sa.Integer(),nullable=False),
    sa.Column("email",sa.String(),nullable=False),
    sa.Column("password",sa.String(),nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("email")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
