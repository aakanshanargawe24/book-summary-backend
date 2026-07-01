import uuid

from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.connection import Base


class JobIterationTelemetry(Base):
    __tablename__ = "job_iteration_telemetry"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    component_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey("job_component_logs.id", ondelete="CASCADE"),
        nullable=False
    )

    iteration_number = Column(Integer, nullable=False)

    chunks_processed_count = Column(Integer, default=0)

    status = Column(String(50), nullable=False)

    llm_tokens_consumed = Column(Integer, default=0)

    execution_time_ms = Column(Integer)

    error_summary = Column(Text)

    executed_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )