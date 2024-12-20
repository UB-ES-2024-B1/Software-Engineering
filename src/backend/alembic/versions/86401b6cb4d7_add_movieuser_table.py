"""Add MovieUser table

Revision ID: 86401b6cb4d7
Revises: 2f3d87a037d3
Create Date: 2024-11-24 13:32:48.822662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86401b6cb4d7'
down_revision: Union[str, None] = '2f3d87a037d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movieuser',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('liked', sa.Boolean(), nullable=True),
    sa.Column('wished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('movie_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movieuser')
    # ### end Alembic commands ###
