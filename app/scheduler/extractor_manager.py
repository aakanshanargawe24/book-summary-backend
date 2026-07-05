from app.database.connection import BookSessionLocal
from app.dao.extraction_jobs_dao import ExtractionJobDao
from app.services.paragraph_extractor import ParagraphExtractor
from app.services.orchestrator import Orchestrator

class ExtractionManager:

    @staticmethod
    def process_book(book_id):

        print(f"Inside process_book: {book_id}")

        db = BookSessionLocal()

        try:

            print(f"Processing Book: {book_id}")

            job = ExtractionJobDao.get_job(
                db=db,
                book_id=book_id
            )

            if job is None:
                print("Job not found")
                return

            Orchestrator.process(
                db=db,
                job_id=job.id,
                book_id=book_id
            )

        except Exception as e:
            print(f"[ExtractionManager Error] {e}")

        finally:
            db.close()