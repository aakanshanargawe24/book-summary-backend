from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_book_db
router = APIRouter()


@router.get("/")
def get_books(db: Session = Depends(get_book_db)):
    return {"message": "All Books"}

@router.post("/")
def create_book(db: Session = Depends(get_book_db)):
    return {"message": "Book Created"}

@router.put("/")
def create_book(db: Session = Depends(get_book_db)):
    return {"message": f"Book {book_id} Updated"}

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_book_db)):
    return {"message": f"Book {book_id} Deleted"}