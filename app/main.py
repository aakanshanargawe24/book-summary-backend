from fastapi import FastAPI

from app.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "message": "Book Processing API is running."
    }