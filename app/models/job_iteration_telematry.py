from sqlalchemy import Column, Integer, Text, ForeignKey, Enum, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.core.enums import IterationStatusType
from app.database.connection import Base


class JobIterationTelemetry(Base):
    __tablename__ = "job_iteration_telemetry"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    component_log_id = Column(
        UUID(as_uuid=True),
        ForeignKey("job_component_logs.id", ondelete="CASCADE"),
        nullable=False
    )

    iteration_number = Column(Integer, nullable=False)
    chunks_processed_count = Column(Integer, default=0)

    # FIX: Native DB validation ke liye name parameter add kiya taaki safe rahe
    status = Column(
        Enum(IterationStatusType, name="iteration_status_type"),
        nullable=False
    )

    llm_tokens_consumed = Column(Integer, default=0)
    execution_time_ms = Column(Integer)
    error_summary = Column(Text)

    executed_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    component_log = relationship(
        "JobComponentLog",
        back_populates="telemetry"
    )

    __table_args__ = (
        UniqueConstraint(
            "component_log_id",
            "iteration_number",
            name="unique_component_iteration"
        ),
    )
