"""Disallow null ChoiceType

Revision ID: 17ef8f7be758
Revises: 45dafbb3f4e1
Create Date: 2024-03-01 00:18:48.971796

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from zou.migrations.utils.base import BaseMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision = "17ef8f7be758"
down_revision = "45dafbb3f4e1"
branch_labels = None
depends_on = None

base = declarative_base()

PROJECT_STYLES = [
    ("2d", "2D Animation"),
    ("3d", "3D Animation"),
    ("2d3d", "2D/3D Animation"),
    ("ar", "Augmented Reality"),
    ("vfx", "VFX"),
    ("stop-motion", "Stop Motion"),
    ("motion-design", "Motion Design"),
    ("archviz", "Archviz"),
    ("commercial", "Commercial"),
    ("catalog", "Catalog"),
    ("immersive", "Immersive Experience"),
    ("nft", "NFT Collection"),
    ("video-game", "Video Game"),
    ("vr", "Virtual Reality"),
]


class Project(base, BaseMixin):
    """
    Describes a production the studio works on.
    """

    __tablename__ = "project"

    name = sa.Column(sa.String(80), nullable=False, unique=True, index=True)
    code = sa.Column(sa.String(80))
    description = sa.Column(sa.Text())
    shotgun_id = sa.Column(sa.Integer)
    file_tree = sa.Column(JSONB)
    data = sa.Column(JSONB)
    has_avatar = sa.Column(sa.Boolean(), default=False)
    fps = sa.Column(sa.String(10), default=25)
    ratio = sa.Column(sa.String(10), default="16:9")
    resolution = sa.Column(sa.String(12), default="1920x1080")
    production_type = sa.Column(sa.String(20), default="short")
    production_style = sa.Column(
        ChoiceType(PROJECT_STYLES), default="2d3d", nullable=False
    )
    start_date = sa.Column(sa.Date())
    end_date = sa.Column(sa.Date())
    man_days = sa.Column(sa.Integer)
    nb_episodes = sa.Column(sa.Integer, default=0)
    episode_span = sa.Column(sa.Integer, default=0)
    max_retakes = sa.Column(sa.Integer, default=0)
    is_clients_isolated = sa.Column(sa.Boolean(), default=False)
    is_preview_download_allowed = sa.Column(sa.Boolean(), default=False)
    is_set_preview_automated = sa.Column(sa.Boolean(), default=False)
    homepage = sa.Column(sa.String(80), default="assets")


ENTITY_STATUSES = [
    ("standby", "Stand By"),
    ("running", "Running"),
    ("complete", "Complete"),
    ("canceled", "Canceled"),
]


STATUSES = [
    ("processing", "Processing"),
    ("ready", "Ready"),
    ("broken", "Broken"),
]

VALIDATION_STATUSES = [
    ("validated", "Validated"),
    ("rejected", "Rejected"),
    ("neutral", "Neutral"),
]


class PreviewFile(base, BaseMixin):
    """
    Describes a file which is aimed at being reviewed. It is not a publication
    neither a working file.
    """

    __tablename__ = "preview_file"
    name = sa.Column(sa.String(250))
    original_name = sa.Column(sa.String(250))
    revision = sa.Column(sa.Integer(), default=1)
    position = sa.Column(sa.Integer(), default=1)
    extension = sa.Column(sa.String(6))
    description = sa.Column(sa.Text())
    path = sa.Column(sa.String(400))
    source = sa.Column(sa.String(40))
    file_size = sa.Column(sa.BigInteger(), default=0)
    status = sa.Column(ChoiceType(STATUSES), default="processing")
    validation_status = sa.Column(
        ChoiceType(VALIDATION_STATUSES), default="neutral", nullable=False
    )
    annotations = sa.Column(JSONB)
    width = sa.Column(sa.Integer(), default=0)
    height = sa.Column(sa.Integer(), default=0)
    duration = sa.Column(sa.Float, default=0)

    task_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("task.id"), index=True
    )
    person_id = sa.Column(UUIDType(binary=False), sa.ForeignKey("person.id"))
    source_file_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("output_file.id")
    )

    __table_args__ = (
        sa.UniqueConstraint("name", "task_id", "revision", name="preview_uc"),
    )

    shotgun_id = sa.Column(sa.Integer, unique=True)

    is_movie = sa.Column(sa.Boolean, default=False)  # deprecated
    url = sa.Column(sa.String(600))  # deprecated
    uploaded_movie_url = sa.Column(sa.String(600))  # deprecated
    uploaded_movie_name = sa.Column(sa.String(150))  # deprecated


class Entity(base, BaseMixin):
    """
    Base model to represent assets, shots, sequences, episodes and scenes.
    They have different meaning but they share the same behaviour toward
    tasks and files.
    """

    __tablename__ = "entity"

    name = sa.Column(sa.String(160), nullable=False)
    code = sa.Column(sa.String(160))  # To store sanitized version of name
    description = sa.Column(sa.String(1200))
    shotgun_id = sa.Column(sa.Integer)
    canceled = sa.Column(sa.Boolean, default=False)

    nb_frames = sa.Column(sa.Integer)  # Specific to shots
    nb_entities_out = sa.Column(sa.Integer, default=0)
    is_casting_standby = sa.Column(sa.Boolean, default=False)

    status = sa.Column(
        ChoiceType(ENTITY_STATUSES), default="running", nullable=False
    )

    project_id = sa.Column(
        UUIDType(binary=False),
    )
    entity_type_id = sa.Column(
        UUIDType(binary=False),
    )

    parent_id = sa.Column(UUIDType(binary=False))  # sequence or episode

    source_id = sa.Column(
        UUIDType(binary=False),
    )  # if the entity is generated from another one (like shots from scene).

    preview_file_id = sa.Column(
        UUIDType(binary=False),
    )
    data = sa.Column(JSONB)

    ready_for = sa.Column(
        UUIDType(binary=False),
    )

    created_by = sa.Column(
        UUIDType(binary=False),
    )


CHANGE_TYPES = [("status", "Status"), ("ready_for", "Ready for")]


class StatusAutomation(
    base,
    BaseMixin,
):
    """
    Status automations are entries that allow to describe changes that
    should automatically apply after a task status is changed.

    For instance, a Modeling task set to done will imply to set the Rigging
    task status to ready and the *ready_for* field to be set at Layout.
    """

    __tablename__ = "status_automation"
    entity_type = sa.Column(sa.String(40), default="asset")

    in_task_type_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("task_type.id"), index=True
    )
    in_task_status_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("task_status.id"), index=True
    )

    out_field_type = sa.Column(
        ChoiceType(CHANGE_TYPES), default="status", nullable=False
    )
    out_task_type_id = sa.Column(
        UUIDType(binary=False), sa.ForeignKey("task_type.id"), index=True
    )
    out_task_status_id = sa.Column(
        UUIDType(binary=False),
        sa.ForeignKey("task_status.id"),
        index=True,
        nullable=True,
    )
    archived = sa.Column(sa.Boolean(), default=False)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("build_job", schema=None) as batch_op:
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=255), nullable=False
        )
        batch_op.alter_column(
            "job_type", existing_type=sa.VARCHAR(length=255), nullable=False
        )

    with op.batch_alter_table("entity", schema=None) as batch_op:
        session = Session(bind=op.get_bind())
        session.query(Entity).where(Entity.status == None).update(
            {
                Entity.status: "running",
            }
        )
        session.commit()
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=255), nullable=False
        )

    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.alter_column(
            "role", existing_type=sa.VARCHAR(length=255), nullable=False
        )

    with op.batch_alter_table("preview_file", schema=None) as batch_op:
        session = Session(bind=op.get_bind())
        session.query(PreviewFile).where(
            PreviewFile.validation_status == None
        ).update(
            {
                PreviewFile.validation_status: "neutral",
            }
        )
        session.commit()
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=255), nullable=False
        )
        batch_op.alter_column(
            "validation_status",
            existing_type=sa.VARCHAR(length=255),
            nullable=False,
        )

    with op.batch_alter_table("project", schema=None) as batch_op:
        session = Session(bind=op.get_bind())
        session.query(Project).where(Project.production_style == None).update(
            {
                Project.production_style: "2d3d",
            }
        )
        session.commit()
        batch_op.alter_column(
            "production_style",
            existing_type=sa.VARCHAR(length=255),
            nullable=False,
        )

    with op.batch_alter_table("status_automation", schema=None) as batch_op:
        session = Session(bind=op.get_bind())
        session.query(StatusAutomation).where(
            StatusAutomation.out_field_type == None
        ).update(
            {
                StatusAutomation.out_field_type: "status",
            }
        )
        session.commit()
        batch_op.alter_column(
            "out_field_type",
            existing_type=sa.VARCHAR(length=255),
            nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("status_automation", schema=None) as batch_op:
        batch_op.alter_column(
            "out_field_type",
            existing_type=sa.VARCHAR(length=255),
            nullable=True,
        )

    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.alter_column(
            "production_style",
            existing_type=sa.VARCHAR(length=255),
            nullable=True,
        )

    with op.batch_alter_table("preview_file", schema=None) as batch_op:
        batch_op.alter_column(
            "validation_status",
            existing_type=sa.VARCHAR(length=255),
            nullable=True,
        )

    with op.batch_alter_table("person", schema=None) as batch_op:
        batch_op.alter_column(
            "role", existing_type=sa.VARCHAR(length=255), nullable=True
        )

    with op.batch_alter_table("entity", schema=None) as batch_op:
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=255), nullable=True
        )

    with op.batch_alter_table("build_job", schema=None) as batch_op:
        batch_op.alter_column(
            "job_type", existing_type=sa.VARCHAR(length=255), nullable=True
        )
        batch_op.alter_column(
            "status", existing_type=sa.VARCHAR(length=255), nullable=True
        )

    # ### end Alembic commands ###
