"""empty message

Revision ID: f56748760a5c
Revises: e44fc998b547
Create Date: 2023-06-17 02:04:25.052270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f56748760a5c'
down_revision = 'e44fc998b547'
branch_labels = None
depends_on = None


from sqlalchemy import text

def upgrade():
    # add new column with default value
    op.add_column('users', sa.Column('date_joined', sa.DateTime(), server_default=text("(now() at time zone 'utc')"), nullable=False))

def downgrade():
    # remove column in downgrade script
    op.drop_column('users', 'date_joined')
