"""create area-site table

Revision ID: 2ccd013af810
Revises: 2eaf44760fe7
Create Date: 2021-12-09 16:51:50.910691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ccd013af810'
down_revision = '2eaf44760fe7'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
        "area_site",
        sa.Column("site_id", sa.String(length=128), nullable=False),
        sa.Column("area_id", sa.String(length=128), nullable=False),
       sa.ForeignKeyConstraint(
            ["site_id"],
            ["site.id"],
        ),
        sa.ForeignKeyConstraint(
            ["area_id"],
            ["area.id"],
        ), 
     )


def downgrade():
    op.drop_table("area_site")
