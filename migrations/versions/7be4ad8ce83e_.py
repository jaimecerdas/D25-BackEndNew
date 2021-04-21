"""empty message

Revision ID: 7be4ad8ce83e
Revises: 0d52ea89113a
Create Date: 2021-04-19 23:02:29.415365

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7be4ad8ce83e'
down_revision = '0d52ea89113a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('favorito_name', sa.String(length=250), nullable=True))
    op.drop_column('favorito', 'planet_name')
    op.drop_column('favorito', 'person_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('person_name', mysql.VARCHAR(length=250), nullable=True))
    op.add_column('favorito', sa.Column('planet_name', mysql.VARCHAR(length=250), nullable=True))
    op.drop_column('favorito', 'favorito_name')
    # ### end Alembic commands ###
