from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class StagingChapterBuffer(Base):
    __tablename__ = "staging_chapter_buffers"

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

    chapter_number = Column(
        Integer,
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    start_page = Column(Integer)

    end_page = Column(Integer)

    macro_setting = Column(Text)

    macro_time_leap = Column(Text)

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    job = relationship("ExtractionJob")

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "chapter_number",
            name="unique_staging_chapter_num"
        ),
    )