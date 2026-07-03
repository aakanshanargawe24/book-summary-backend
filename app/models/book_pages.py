from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class BookPage(Base):
    __tablename__ = 'book_pages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_number = Column(Integer, nullable=False)
    book_id = Column(UUID(as_uuid=True), ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    raw_content = Column(Text, nullable=True)

    # Relationship back to book
    book = relationship("Book", back_populates="pages")

