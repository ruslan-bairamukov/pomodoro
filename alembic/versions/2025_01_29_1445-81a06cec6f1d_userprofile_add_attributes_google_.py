"""UserProfile: add attributes: google_access_token, yandex_access_token, email, name

Revision ID: 81a06cec6f1d
Revises: 9f92a1395868
Create Date: 2025-01-29 14:45:21.313203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81a06cec6f1d'
down_revision: Union[str, None] = '9f92a1395868'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('google_access_token', sa.String(), nullable=True))
    op.add_column('user_profile', sa.Column('yandex_access_token', sa.String(), nullable=True))
    op.add_column('user_profile', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user_profile', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'name')
    op.drop_column('user_profile', 'email')
    op.drop_column('user_profile', 'yandex_access_token')
    op.drop_column('user_profile', 'google_access_token')
    # ### end Alembic commands ###
