from fastapi import FastAPI

from app.lifespan import lifespan
from app.routes.book_routes import router
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(lifespan=lifespan)


app.add_middleware(AuthMiddleware)


app.include_router(
    router,
    prefix="/books"
)


@app.get("/")
def home():
    return {
        "message": "Application Running"
    }