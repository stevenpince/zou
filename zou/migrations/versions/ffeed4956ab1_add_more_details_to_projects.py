"""add more details to projects

Revision ID: ffeed4956ab1
Revises: e839d6603c09
Create Date: 2021-01-18 18:06:34.230687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffeed4956ab1"
down_revision = "e839d6603c09"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "project",
        "description",
        type_=sa.Text(),
        existing_type=sa.String(length=200),
        nullable=True,
    )
    op.add_column(
        "project", sa.Column("episode_span", sa.Integer(), nullable=True)
    )
    op.add_column(
        "project", sa.Column("nb_episodes", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("project", "nb_episodes")
    op.drop_column("project", "episode_span")
    op.alter_column(
        "project",
        "description",
        type_=sa.String(length=200),
        existing_type_=sa.Text(),
        nullable=True,
    )
    # ### end Alembic commands ###
