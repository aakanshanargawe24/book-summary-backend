from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_books():
    return {"message": "All Books"}


@router.post("/")
def create_book():
    return {"message": "Book Created"}


@router.put("/{book_id}")
def update_book(book_id: int):
    return {"message": f"Book {book_id} Updated"}


@router.delete("/{book_id}")
def delete_book(book_id: int):
    return {"message": f"Book {book_id} Deleted"}