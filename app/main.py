from fastapi import FastAPI

from app.lifespan import lifespan
from app.routes.book_routes import router as book_router
app = FastAPI(
    lifespan=lifespan
)

app.include_router(
    book_router,
    prefix="/books",
    tags=["Books"]
)
@app.get("/")
def home():
    return {
        "message": "Book Processing API is running."
    }
