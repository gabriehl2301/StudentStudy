"""Add Log model

Revision ID: 69376c4f24c0
Revises: 04b8529ec3e9
Create Date: 2025-01-31 05:19:13.798188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69376c4f24c0'
down_revision = '04b8529ec3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('action', sa.String(length=255), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    # ### end Alembic commands ###
