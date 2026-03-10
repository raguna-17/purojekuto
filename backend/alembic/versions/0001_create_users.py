"""init

Revision ID: 8223ca4d8b70
Revises: 
Create Date: 2026-03-09 10:40:42.435434
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8223ca4d8b70'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )
    # username 列や index、constraint は別 migration にする


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')