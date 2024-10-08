"""adding user domain

Revision ID: 07e215d55c18
Revises: b3463de3ec5d
Create Date: 2024-09-16 21:52:40.111997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07e215d55c18'
down_revision = 'b3463de3ec5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userdomain', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('userdomain')

    # ### end Alembic commands ###
