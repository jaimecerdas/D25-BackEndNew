"""empty message

Revision ID: 611b650a323f
Revises: 143610a90311
Create Date: 2021-04-18 00:27:36.582124

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '611b650a323f'
down_revision = '143610a90311'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('person_name', sa.String(length=250), nullable=True))
    op.alter_column('favorito', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.drop_constraint('favorito_ibfk_3', 'favorito', type_='foreignkey')
    op.drop_constraint('favorito_ibfk_2', 'favorito', type_='foreignkey')
    op.drop_constraint('favorito_ibfk_1', 'favorito', type_='foreignkey')
    op.drop_column('favorito', 'person_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('favorito', sa.Column('person_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('favorito_ibfk_1', 'favorito', 'person', ['person_id'], ['id'])
    op.create_foreign_key('favorito_ibfk_2', 'favorito', 'planet', ['planet_id'], ['id'])
    op.create_foreign_key('favorito_ibfk_3', 'favorito', 'user', ['user_id'], ['id'])
    op.alter_column('favorito', 'user_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.drop_column('favorito', 'person_name')
    # ### end Alembic commands ###
