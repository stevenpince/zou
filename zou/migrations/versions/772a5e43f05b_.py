"""empty message

Revision ID: 772a5e43f05b
Revises: af1790868e2c
Create Date: 2019-03-10 16:47:27.816163

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlalchemy_utils
import uuid

# revision identifiers, used by Alembic.
revision = "772a5e43f05b"
down_revision = "af1790868e2c"
branch_labels = None
depends_on = None

TYPES = [
    ("comment", "Comment"),
    ("mention", "Mention"),
    ("assignation", "Assignation"),
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "comment_mentions",
        sa.Column(
            "comment",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.Column(
            "person",
            sqlalchemy_utils.types.uuid.UUIDType(binary=False),
            default=uuid.uuid4,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["comment"],
            ["comment.id"],
        ),
        sa.ForeignKeyConstraint(
            ["person"],
            ["person.id"],
        ),
        sa.PrimaryKeyConstraint("comment", "person"),
    )
    op.add_column(
        "notification",
        sa.Column(
            "type",
            sqlalchemy_utils.types.choice.ChoiceType(TYPES),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("notification", "type")
    op.drop_table("comment_mentions")
    # ### end Alembic commands ###
