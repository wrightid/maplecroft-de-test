"""create area table

Revision ID: 2eaf44760fe7
Revises: 8aabb1c86272
Create Date: 2021-12-09 16:51:33.380088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2eaf44760fe7'
down_revision = '8aabb1c86272'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        "area",
        sa.Column("id", sa.String(length=128), nullable=False),
        sa.Column("shape_name", sa.String(length=128), nullable=True),
        sa.Column("shape_group", sa.String(length=32), nullable=False),
        sa.Column("shape_type", sa.String(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("area")
