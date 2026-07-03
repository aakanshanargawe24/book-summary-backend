from sqlalchemy import (
    Column,
    Boolean,
    ForeignKey,
    Enum,
    TIMESTAMP,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base
from app.core.enums import JobStatusType


class ExtractionJob(Base):
    __tablename__ = "extraction_jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    is_processed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    last_successful_run_at = Column(
        TIMESTAMP(timezone=True)
    )

    current_status = Column(
        Enum(JobStatusType),
        nullable=False,
        default=JobStatusType.PROCESSING
    )

    started_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    ended_at = Column(
        TIMESTAMP(timezone=True)
    )

    book = relationship(
        "Book",
        back_populates="extraction_job"
    )

    component_logs = relationship(
        "JobComponentLog",
        back_populates="job",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index(
            "idx_unique_active_book_job",
            "book_id",
            unique=True
        ),
    )