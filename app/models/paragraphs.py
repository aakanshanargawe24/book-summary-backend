from sqlalchemy import (
    Column,
    Integer,

    Text,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP, TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from pgvector.sqlalchemy import Vector  # Terminal me 'pip install pgvector' hona zaroori hai

from app.database.connection import Base


class Paragraph(Base):
    __tablename__ = "paragraphs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    section_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sections.id", ondelete="SET NULL"),
        nullable=True
    )

    book_id = Column(
        UUID(as_uuid=True),
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False
    )

    global_sequence = Column(Integer, nullable=False)
    start_page = Column(Integer, nullable=False)
    end_page = Column(Integer, nullable=False)
    raw_text = Column(Text, nullable=False)

    physical_character_tracking = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    mental_emotional_state = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    rule_enforcement = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    causal_chains = Column(
        JSONB,
        server_default=text("'[]'::jsonb")
    )

    embedding = Column(Vector(1536))
    search_vector = Column(TSVECTOR)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationships
    section = relationship(
        "Section",
        back_populates="paragraphs"
    )

    book = relationship(
        "Book",
        back_populates="paragraphs"
    )

    __table_args__ = (
        UniqueConstraint(
            "book_id",
            "global_sequence",
            name="unique_book_global_seq"
        ),
        Index(
            "idx_paragraphs_section_id",
            "section_id"
        ),
        Index(
            "idx_paragraphs_global_sequence",
            "global_sequence"
        ),
        Index(
            "idx_paragraphs_causal_chains_gin",
            "causal_chains",
            postgresql_using="gin"
        ),
        # FIX: HNSW index syntax ko postgresql_with ke sath clean kiya
        Index(
            "idx_paragraphs_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"withops": text("vector_cosine_ops")}
        ),
    )