"""Add unique constraint to the field username in UserProfile sqlalchemy model

Revision ID: c6067958db1a
Revises: 46b22c0b1683
Create Date: 2025-01-22 18:36:17.750751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6067958db1a'
down_revision: Union[str, None] = '46b22c0b1683'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'user_profile', ['username'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_profile', type_='unique')
    # ### end Alembic commands ###
