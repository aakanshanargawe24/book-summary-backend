from contextlib import asynccontextmanager

from app.database.connection import Base, book_engine
# Import all models
from app.models import *


@asynccontextmanager
async def lifespan(app):
    print("Creating database tables...")

    Base.metadata.create_all(bind=book_engine)

    print("Database is ready.")

    yield

    print("Application shutting down...")
