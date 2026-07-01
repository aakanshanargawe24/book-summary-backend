from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models.books import Book


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Application Starting...")

    Base.metadata.create_all(bind=engine)

    yield

    print("Application Closing...")