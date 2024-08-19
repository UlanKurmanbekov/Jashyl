"""add health, renamed field to pet table

Revision ID: 82b6aa1b1953
Revises: 52c8626f1b15
Create Date: 2024-08-20 01:04:25.995802

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "82b6aa1b1953"
down_revision: Union[str, None] = "52c8626f1b15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("pets", sa.Column("health", sa.Integer(), nullable=False))
    op.add_column("pets", sa.Column("renamed", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("pets", "renamed")
    op.drop_column("pets", "health")
    # ### end Alembic commands ###
