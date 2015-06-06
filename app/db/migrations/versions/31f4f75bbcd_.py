# flake8: noqa
"""empty message

Revision ID: 31f4f75bbcd
Revises: 1cc45bbe916
Create Date: 2015-06-05 12:34:48.504598

"""

# revision identifiers, used by Alembic.
revision = '31f4f75bbcd'
down_revision = '1cc45bbe916'


from alembic import op
import sqlalchemy as sa



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rsvp', sa.Column('menu_choice', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rsvp', 'menu_choice')
    ### end Alembic commands ###
