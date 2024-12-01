"""merge heads

Revision ID: 831f26aabcc6
Revises: 86401b6cb4d7, f690524b5588
Create Date: 2024-11-30 02:49:43.106483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '831f26aabcc6'
down_revision: Union[str, None] = ('86401b6cb4d7', 'f690524b5588')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
