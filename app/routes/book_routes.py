from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import cast  # <-- STEP 1: cast import kiya
from sqlalchemy.dialects.postgresql import UUID  # <-- STEP 2: UUID dialect import kiya

from app.database.connection import get_book_db
from app.models.book_pages import BookPage
from app.models.books import Book
from app.clients.llm import LLMClient

router = APIRouter()


@router.get("/")
def get_books(db: Session = Depends(get_book_db)):
    return {"message": "All Books"}


@router.post("/")
def create_book(db: Session = Depends(get_book_db)):
    return {"message": "Book Created"}


@router.put("/{book_id}")
def update_book(book_id: str, db: Session = Depends(get_book_db)):
    return {"message": f"Book {book_id} Updated"}


@router.delete("/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_book_db)):
    return {"message": f"Book {book_id} Deleted"}


@router.post("/{book_id}/generate-summary")
async def generate_summary(
        book_id: str,
        db: Session = Depends(get_book_db)
):
    print("Database session created")

    # Step 1: Check if book exists using explicit cast
    # (Yeh string book_id ko safely database driver ke liye native UUID mein cast karega)
    book = db.query(Book).filter(Book.id == cast(book_id, UUID)).first()
    print("Book fetched from database")

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    # Step 2: Fetch all pages using explicit cast
    pages = (
        db.query(BookPage)
        .filter(BookPage.book_id == cast(book_id, UUID))
        .order_by(BookPage.page_number)
        .all()
    )

    # Step 3: Combine raw content
    book_text = "\n".join(
        page.raw_content or ""
        for page in pages
    )

    if not book_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book has no page content to summarize."
        )

    # Step 4: Call Gemini
    try:
        llm_client = LLMClient()
        summary = llm_client.generate_content(
            prompt=f"Summarize the following book concisely:\n\n{book_text}"
        )
    except Exception as llm_err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to generate summary via Gemini: {str(llm_err)}"
        )

    # Step 5: Return response
    return {
        "book_id": str(book.id),
        "title": book.title,
        "summary": summary
    }