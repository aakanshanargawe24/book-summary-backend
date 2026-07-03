from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    TIMESTAMP,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class StagingSectionBuffer(Base):
    __tablename__ = "staging_section_buffers"

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

    section_number = Column(
        Integer,
        nullable=False
    )

    name = Column(String(255))
    start_page = Column(Integer)
    end_page = Column(Integer)

    associated_para_sequences = Column(
        ARRAY(Integer),
        server_default=text("'{}'")
    )

    focal_characters = Column(
        ARRAY(Text),
        server_default=text("'{}'")
    )

    current_location = Column(Text)
    time_anchor = Column(String(100))

    # FIX: onupdate add kiya taaki row modify hote hi time badal jaye
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    # FIX: ExtractionJob ke sath multi-directional link maintain kiya
    job = relationship("ExtractionJob", back_populates="staging_sections")

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "section_number",
            name="unique_staging_section_num"
        ),
    )
