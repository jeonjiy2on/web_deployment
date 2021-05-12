"""empty message

Revision ID: 6a3ba023da5a
Revises: 
Create Date: 2021-04-08 10:17:51.680165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3ba023da5a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('input_',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('input_img', sa.String(length=100), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('model_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_name', sa.String(length=100), nullable=False),
    sa.Column('model_detail', sa.Text(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inputimage_id', sa.Integer(), nullable=True),
    sa.Column('return_img', sa.String(length=100), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['inputimage_id'], ['input_.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_table('model_list')
    op.drop_table('input_')
    # ### end Alembic commands ###
