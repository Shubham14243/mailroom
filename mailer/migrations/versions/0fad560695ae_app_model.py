"""App Model

Revision ID: 0fad560695ae
Revises: 923d880a0d27
Create Date: 2024-08-09 00:42:00.956738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fad560695ae'
down_revision = '923d880a0d27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app',
    sa.Column('app_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('app_name', sa.String(length=100), nullable=False),
    sa.Column('api_key', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('app_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app')
    # ### end Alembic commands ###
