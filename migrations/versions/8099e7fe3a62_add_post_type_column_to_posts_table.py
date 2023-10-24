"""Add post-type column to posts table

Revision ID: 8099e7fe3a62
Revises: dde782d264aa
Create Date: 2023-07-10 14:24:18.935076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8099e7fe3a62'
down_revision = 'dde782d264aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_type', sa.Text(), nullable=True))
        batch_op.alter_column('votes',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('votes',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('0'))
        batch_op.drop_column('post_type')

    # ### end Alembic commands ###
