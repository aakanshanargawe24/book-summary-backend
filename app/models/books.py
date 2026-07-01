from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    total_pages = Column(Integer)