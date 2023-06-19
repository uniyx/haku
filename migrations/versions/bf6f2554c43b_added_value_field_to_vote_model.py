"""Added value field to Vote model

Revision ID: bf6f2554c43b
Revises: 6e7a3d29f64a
Create Date: 2023-06-19 15:26:25.932248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf6f2554c43b'
down_revision = '6e7a3d29f64a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('value', sa.Integer(), nullable=True))
        batch_op.drop_column('vote')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('votes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vote', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('value')

    # ### end Alembic commands ###