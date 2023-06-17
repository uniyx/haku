"""empty message

Revision ID: 37dc1916bfa7
Revises: 777efb503aef
Create Date: 2023-06-17 13:55:33.429892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37dc1916bfa7'
down_revision = '777efb503aef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('communities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.alter_column('community_id',
               existing_type=sa.TEXT(),
               type_=sa.Integer(),
               nullable=False)
        batch_op.create_foreign_key(None, 'communities', ['community_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('community_id',
               existing_type=sa.Integer(),
               type_=sa.TEXT(),
               nullable=True)

    op.drop_table('communities')
    # ### end Alembic commands ###