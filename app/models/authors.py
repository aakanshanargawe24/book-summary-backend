from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database.connection import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuid_generate_v4()")
    )

    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    biography = Column(Text)
    profile_image_url = Column(Text)


    metadata_json = Column(
        "metadata",
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    books = relationship(
        "Book",
        back_populates="author"
    )