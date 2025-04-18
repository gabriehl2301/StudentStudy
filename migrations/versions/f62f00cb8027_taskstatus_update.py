"""taskstatus update

Revision ID: f62f00cb8027
Revises: 2d5ad98973ef
Create Date: 2025-02-11 08:33:48.426191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f62f00cb8027'
down_revision = '2d5ad98973ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=9),
               type_=sa.Enum('Active', 'Cancelled', 'Complete', 'Not_Started', name='taskstatus'),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.Enum('Active', 'Cancelled', 'Complete', 'Not_Started', name='taskstatus'),
               type_=sa.VARCHAR(length=9),
               existing_nullable=False)

    # ### end Alembic commands ###
