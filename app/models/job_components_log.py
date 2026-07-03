from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Enum,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base
from app.core.enums import LayerTypeEnum, ComponentStatusType


class JobComponentLog(Base):
    __tablename__ = "job_component_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extraction_jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    layer_type = Column(
        Enum(LayerTypeEnum),
        nullable=False
    )

    current_global_sequence = Column(
        Integer,
        nullable=False,
        default=0
    )

    current_page_cursor = Column(Integer)

    current_paragraph_cursor = Column(Integer)

    current_section_cursor = Column(Integer)

    status = Column(
        Enum(ComponentStatusType),
        nullable=False,
        default=ComponentStatusType.PENDING
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    job = relationship(
        "ExtractionJob",
        back_populates="component_logs"
    )

    telemetry = relationship(
        "JobIterationTelemetry",
        back_populates="component_log",
        cascade="all, delete-orphan"
    )
    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "layer_type",
            name="unique_job_layer"
        ),
    )
