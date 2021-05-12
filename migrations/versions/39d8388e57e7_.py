"""empty message

Revision ID: 39d8388e57e7
Revises: 7908f02934f7
Create Date: 2021-04-15 09:19:20.392935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39d8388e57e7'
down_revision = '7908f02934f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upload_info', sa.Column('image_name', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('upload_info', 'image_name')
    # ### end Alembic commands ###
