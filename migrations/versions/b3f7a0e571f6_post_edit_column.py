"""Post edit column

Revision ID: b3f7a0e571f6
Revises: daa33c19d397
Create Date: 2023-06-18 20:44:18.140343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3f7a0e571f6'
down_revision = 'daa33c19d397'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_edited', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('date_edited')

    # ### end Alembic commands ###
