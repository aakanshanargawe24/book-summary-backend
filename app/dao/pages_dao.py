from uuid import UUID

from sqlalchemy.orm import Session

from app.models.book_pages import BookPage


class PagesDao:

    @staticmethod
    def get_book_details(
        db: Session,
        book_id: UUID
    ):

        return (
            db.query(BookPage)
            .filter(BookPage.book_id == book_id)
            .order_by(BookPage.page_number)
            .all()
        )

    @staticmethod
    def save_pages(
            db: Session,
            book_id: UUID,
            pages
    ):
        page_objects = []

        for page in pages:
            page_objects.append(
                BookPage(
                    book_id=book_id,
                    page_number=page["page_number"],
                    raw_content=page["raw_content"]
                )
            )

        db.add_all(page_objects)
        db.commit()

        return page_objects

