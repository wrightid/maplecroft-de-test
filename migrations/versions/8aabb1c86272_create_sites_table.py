"""create sites table

Revision ID: 8aabb1c86272
Revises: 3c403aee5d08
Create Date: 2021-12-08 14:05:01.486607

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8aabb1c86272'
down_revision = '3c403aee5d08'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "site",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("country", sa.String(length=2), nullable=False),
        # String is the only way to accurately store in SQLLite
        sa.Column("latitude", sa.String(length=20), nullable=False),
        sa.Column("longitude", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("site")
