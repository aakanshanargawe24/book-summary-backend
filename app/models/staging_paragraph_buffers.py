from sqlalchemy import (
    Column,
    Integer,
    Text,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class StagingParagraphBuffer(Base):
    __tablename__ = "staging_paragraph_buffers"

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

    global_sequence = Column(
        Integer,
        nullable=False
    )

    start_page = Column(
        Integer,
        nullable=False
    )

    end_page = Column(
        Integer,
        nullable=False
    )

    buffered_text = Column(
        Text,
        nullable=False
    )

    is_complete = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    job = relationship(
        "ExtractionJob"
    )

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "global_sequence",
            name="unique_staging_para_seq"
        ),
    )