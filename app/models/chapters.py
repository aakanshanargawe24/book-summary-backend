from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )

    chapter_number = Column(Integer, nullable=False)

    name = Column(String(255), nullable=False)

    start_page = Column(Integer)

    end_page = Column(Integer)

    events = Column(
        JSONB,
        server_default=text("'[]'::jsonb")
    )

    plot_anchors_and_threads = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    world_state_rules = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    book = relationship(
        "Book",
        back_populates="chapters"
    )

    sections = relationship(
        "Section",
        back_populates="chapter"
    )

    __table_args__ = (
        UniqueConstraint(
            "book_id",
            "chapter_number",
            name="unique_book_chapter"
        ),
        Index(
            "idx_chapters_book_id",
            "book_id"
        ),
    )