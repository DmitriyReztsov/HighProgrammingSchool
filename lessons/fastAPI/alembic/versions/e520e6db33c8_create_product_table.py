"""create product table

Revision ID: e520e6db33c8
Revises: 2c0fddf8213b
Create Date: 2023-12-25 10:32:51.750261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e520e6db33c8"
down_revision: Union[str, None] = "2c0fddf8213b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("product", sa.Column("description", sa.String(length=150), nullable=True))
    op.execute('UPDATE product SET description = "Not provided" WHERE description IS NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("product", "description")
    # ### end Alembic commands ###