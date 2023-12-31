"""empty message

Revision ID: 47007aa0a697
Revises: e8b0a42dfc5a
Create Date: 2023-06-17 02:26:15.566971

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '47007aa0a697'
down_revision = 'e8b0a42dfc5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('date_joined',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('date_joined',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)

    # ### end Alembic commands ###
