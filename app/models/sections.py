from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    chapter_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chapters.id", ondelete="SET NULL"),
        nullable=True
    )

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )

    section_number = Column(Integer, nullable=False)

    name = Column(String(255))

    start_page = Column(Integer)

    end_page = Column(Integer)

    characters = Column(
        JSONB,
        server_default=text("'[]'::jsonb")
    )

    character_relationships = Column(
        JSONB,
        server_default=text("'[]'::jsonb")
    )

    information_asymmetry = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    chapter = relationship(
        "Chapter",
        back_populates="sections"
    )

    book = relationship(
        "Book",
        back_populates="sections"
    )

    paragraphs = relationship(
        "Paragraph",
        back_populates="section"
    )

    __table_args__ = (
        UniqueConstraint(
            "book_id",
            "section_number",
            name="unique_book_section"
        ),
        Index(
            "idx_sections_chapter_id",
            "chapter_id"
        ),
        Index(
            "idx_sections_characters_gin",
            "characters",
            postgresql_using="gin"
        ),
    )
