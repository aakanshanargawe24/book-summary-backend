from contextlib import asynccontextmanager

from app.database.connection import Base, book_engine
# Import all models
from app.models import *
from app.scheduler.paragraph_scheduler import (
    start_scheduler,
    stop_scheduler,
)

@asynccontextmanager
async def lifespan(app):
    print("Creating database tables...")

    Base.metadata.create_all(bind=book_engine)

    print("Database is ready.")
    start_scheduler()
    yield

    print("Application shutting down...")

    stop_scheduler()

