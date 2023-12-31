"""empty message

Revision ID: 2b9aaed0d1e3
Revises: cb957c60d4ed
Create Date: 2023-12-08 14:51:40.125499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b9aaed0d1e3'
down_revision = 'cb957c60d4ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isAdmin', sa.Boolean(), nullable=False))
        batch_op.drop_column('role')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.BOOLEAN(), nullable=False))
        batch_op.drop_column('isAdmin')

    # ### end Alembic commands ###
