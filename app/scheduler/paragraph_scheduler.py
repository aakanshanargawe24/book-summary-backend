
from apscheduler.schedulers.background import BackgroundScheduler

from app.database.connection import BookSessionLocal
from app.dao.extraction_jobs_dao import ExtractionJobDao
from app.scheduler.extractor_manager import ExtractionManager
import threading
scheduler = BackgroundScheduler()


def process_extraction_jobs():

    with BookSessionLocal() as book_db:

        try:

            jobs = ExtractionJobDao.get_all_jobs(book_db)

            for job in jobs:

                print(
                    f"Book: {job.book_id} | "
                    f"Status: {job.current_status}"
                )

                if str(job.current_status).lower().endswith("processing"):


                    thread = threading.Thread(
                        target=ExtractionManager.process_book,
                        args=(job.book_id,)
                    )

                    thread.start()
        except Exception as e:

            print(f"[Scheduler Error] {e}")


def start_scheduler():

    scheduler.add_job(
        process_extraction_jobs,
        trigger="interval",
        seconds=10,
        id="book_count_scheduler",
        replace_existing=True
    )

    if not scheduler.running:
        scheduler.start()

    print("Scheduler Started")


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown()

    print("Scheduler Stopped")