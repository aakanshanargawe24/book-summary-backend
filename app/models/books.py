from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("authors.id", ondelete="RESTRICT"),
        nullable=False
    )

    title = Column(String(255), nullable=False)
    total_pages = Column(Integer, nullable=False)
    cover_image_url = Column(Text)
    is_ready = Column(Text)
    publication_year = Column(Integer)


    metadata_json = Column(
        "metadata",
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )


    author = relationship("Author", back_populates="books")

    pages = relationship(
        "BookPage",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    chapters = relationship(
        "Chapter",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    sections = relationship(
        "Section",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    paragraphs = relationship(
        "Paragraph",
        back_populates="book",
        cascade="all, delete-orphan"
    )

    extraction_job = relationship(
        "ExtractionJob",
        back_populates="book",
        uselist=False,
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_books_author_id", "author_id"),
    )