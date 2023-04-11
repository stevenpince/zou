"""empty message

Revision ID: f995b28fb749
Revises: 38baa9a23b3d
Create Date: 2018-09-13 13:40:05.558866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f995b28fb749"
down_revision = "38baa9a23b3d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "project", sa.Column("fps", sa.String(length=10), nullable=True)
    )
    op.add_column(
        "project", sa.Column("ratio", sa.String(length=10), nullable=True)
    )
    op.add_column(
        "project", sa.Column("resolution", sa.String(length=12), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "resolution")
    op.drop_column("project", "ratio")
    op.drop_column("project", "fps")
    # ### end Alembic commands ###
