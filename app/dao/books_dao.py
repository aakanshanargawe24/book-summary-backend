from sqlalchemy.orm import Session

from app.models.books import Book


class BooksDao:

    @staticmethod
    def create_book(
        db: Session,
        book: Book
    ):

        db.add(book)
        db.commit()
        db.refresh(book)

        return book

    @staticmethod
    def get_book(
        db: Session,
        book_id
    ):

        return (
            db.query(Book)
            .filter(Book.id == book_id)
            .first()
        )