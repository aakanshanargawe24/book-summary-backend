from sqlalchemy.orm import Session

from app.models.extraction_jobs import ExtractionJob




class ExtractionJobDao:

    @staticmethod
    def create_job(
        db: Session,
        job: ExtractionJob
    ):

        db.add(job)

        db.commit()

        db.refresh(job)

        return job

    @staticmethod
    def get_job(
        db: Session,
        book_id
    ):

        return (
            db.query(ExtractionJob)
            .filter(ExtractionJob.book_id == book_id)
            .first()
        )

    @staticmethod
    def get_all_jobs(db: Session):
        return db.query(ExtractionJob).all()

    @staticmethod
    def get_all_jobs(db: Session):
        return db.query(ExtractionJob).all()