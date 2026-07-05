from sqlalchemy.orm import Session

from app.models.paragraphs import Paragraph


class ParagraphDao:

    @staticmethod
    def save_paragraphs(
        db: Session,
        paragraphs
    ):

        paragraph_objects = []

        for paragraph in paragraphs:

            paragraph_objects.append(
                Paragraph(
                    book_id=paragraph["book_id"],
                    global_sequence=paragraph["global_sequence"],
                    start_page=paragraph["start_page"],
                    end_page=paragraph["end_page"],
                    raw_text=paragraph["raw_text"]
                )
            )

        db.add_all(paragraph_objects)
        db.commit()

        return paragraph_objects