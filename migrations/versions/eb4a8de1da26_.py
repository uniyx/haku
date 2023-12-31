"""empty message

Revision ID: eb4a8de1da26
Revises: 53df43122f06
Create Date: 2023-06-17 02:25:04.550963

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb4a8de1da26'
down_revision = '53df43122f06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('date_joined')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_joined', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
