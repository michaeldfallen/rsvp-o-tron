# flake8: noqa
"""empty message

Revision ID: 4b688e9382
Revises: None
Create Date: 2015-03-26 12:50:22.408936

"""

# revision identifiers, used by Alembic.
revision = '4b688e9382'
down_revision = None


from alembic import op
import sqlalchemy as sa



def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('guest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('guest')
    op.drop_table('invite')
    ### end Alembic commands ###
