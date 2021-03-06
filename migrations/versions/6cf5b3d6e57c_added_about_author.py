"""added about author

Revision ID: 6cf5b3d6e57c
Revises: 1d8a0f499d8c
Create Date: 2022-04-24 16:35:26.653923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cf5b3d6e57c'
down_revision = '1d8a0f499d8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_author', sa.Text(length=500), nullable=True))
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'about_author')
    # ### end Alembic commands ###
