"""alter users table

Revision ID: 9223ca4d8b71
Revises: 8223ca4d8b70
Create Date: 2026-03-10 12:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '9223ca4d8b71'
down_revision = '8223ca4d8b70'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # DROP / CREATE CONSTRAINT, INDEX 操作
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.drop_column('users', 'username')


def downgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(50), nullable=False))
    op.drop_index('ix_users_email', table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.create_unique_constraint('users_email_key', 'users', ['email'])