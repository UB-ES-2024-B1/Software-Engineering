"""Add ListType table

Revision ID: f792636c554c
Revises: 71ffd0647d58
Create Date: 2024-12-07 22:51:34.323421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = 'f792636c554c'
down_revision: Union[str, None] = '71ffd0647d58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_by_user_email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listtype_created_by_user_email'), 'listtype', ['created_by_user_email'], unique=False)
    op.create_index(op.f('ix_listtype_name'), 'listtype', ['name'], unique=False)
    op.create_table('movielist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_type_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['list_type_id'], ['listtype.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movielist')
    op.drop_index(op.f('ix_listtype_name'), table_name='listtype')
    op.drop_index(op.f('ix_listtype_created_by_user_email'), table_name='listtype')
    op.drop_table('listtype')
    # ### end Alembic commands ###
