"""Add color and price columns to cars and create index on brand

Revision ID: ffb24838c67f
Revises: ba898ff7ed44
Create Date: 2025-01-04 17:11:54.471571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffb24838c67f'
down_revision: Union[str, None] = 'ba898ff7ed44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
