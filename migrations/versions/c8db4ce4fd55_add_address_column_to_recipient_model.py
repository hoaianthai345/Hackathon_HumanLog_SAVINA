"""Add address column to Recipient model

Revision ID: c8db4ce4fd55
Revises: 015b3b553818
Create Date: 2025-04-19 14:09:09.386861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8db4ce4fd55'
down_revision = '015b3b553818'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipient', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipient', schema=None) as batch_op:
        batch_op.drop_column('address')

    # ### end Alembic commands ###
