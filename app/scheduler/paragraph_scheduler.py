from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

from app.database.connection import BookSessionLocal
from app.models.books import Book

scheduler = BackgroundScheduler()


def log_book_count():

    with BookSessionLocal() as book_db:

        try:
            total_books = book_db.query(
                func.count(Book.id)
            ).scalar()

            print(f"[Scheduler] Total Books: {total_books}")

        except Exception as e:
            print(f"[Scheduler Error] Failed to fetch book count: {e}")


def start_scheduler():

    scheduler.add_job(
        log_book_count,
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