import uuid

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func

from app.database.connection import Base


class StagingSectionBuffer(Base):
    __tablename__ = "staging_section_buffers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    job_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extraction_jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    section_number = Column(Integer, nullable=False)

    name = Column(String(255))

    start_page = Column(Integer)

    end_page = Column(Integer)

    associated_para_sequences = Column(ARRAY(Integer), default=list)

    focal_characters = Column(ARRAY(Text), default=list)

    current_location = Column(Text)

    time_anchor = Column(String(100))

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )