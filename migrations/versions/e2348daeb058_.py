"""empty message

Revision ID: e2348daeb058
Revises: 2a574c0d198a
Create Date: 2021-04-14 15:43:10.501238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2348daeb058'
down_revision = '2a574c0d198a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upload_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_name', sa.String(length=100), nullable=False),
    sa.Column('image_list', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upload_info')
    # ### end Alembic commands ###