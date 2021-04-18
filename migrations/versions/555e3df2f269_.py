"""empty message

Revision ID: 555e3df2f269
Revises: 611b650a323f
Create Date: 2021-04-18 00:29:53.769482

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '555e3df2f269'
down_revision = '611b650a323f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('planet_name', sa.String(length=250), nullable=True))
    op.add_column('favorito', sa.Column('user_email', sa.String(length=250), nullable=True))
    op.drop_column('favorito', 'user_id')
    op.drop_column('favorito', 'planet_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('planet_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('favorito', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('favorito', 'user_email')
    op.drop_column('favorito', 'planet_name')
    # ### end Alembic commands ###
