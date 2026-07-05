import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
)

from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.database.connection import get_book_db
from app.models.books import Book
from app.clients.llm import LLMClient
from app.dao.pages_dao import PagesDao
from app.dao.books_dao import BooksDao
from app.utils.ocr_utils import OCRUtils
from app.models.extraction_jobs import ExtractionJob
from app.dao.extraction_jobs_dao import ExtractionJobDao
router = APIRouter()


@router.get("/")
def get_books(db: Session = Depends(get_book_db)):
    return {"message": "All Books"}


@router.post("/")
async def upload_book(
    file: UploadFile = File(...),        # <-- Added the missing comma here
    db: Session = Depends(get_book_db)   # <-- This is now syntactically perfect
):
    # Create temp folder if it doesn't exist
    os.makedirs("temp", exist_ok=True)

    # Save uploaded PDF
    file_path = f"temp/{file.filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read PDF using OCR utility
    pages = OCRUtils.pdf_to_pages(file_path)
    book = Book(
        author_id="d0f8e70f-0680-4455-beda-e27539ad8788",
        title=file.filename.replace(".pdf", ""),
        total_pages=len(pages)
    )

    book = BooksDao.create_book(
        db=db,
        book=book
    )
    PagesDao.save_pages(
        db=db,
        book_id=book.id,
        pages=pages
    )
    job = ExtractionJob(
        book_id=book.id
    )

    ExtractionJobDao.create_job(
        db=db,
        job=job
    )
    return {
        "message": "Book Created Successfully",
        "book_id": str(book.id),
        "title": book.title,
        "total_pages": book.total_pages
    }



@router.put("/{book_id}")
def update_book(
    book_id: str,
    db: Session = Depends(get_book_db)
):
    return {
        "message": f"Book {book_id} Updated"
    }


@router.delete("/{book_id}")
def delete_book(
    book_id: str,
    db: Session = Depends(get_book_db)
):
    return {
        "message": f"Book {book_id} Deleted"
    }


@router.post("/{book_id}/generate-summary")
async def generate_summary(
    book_id: str,
    db: Session = Depends(get_book_db)
):

    print("Database session created")

    book = (
        db.query(Book)
        .filter(Book.id == cast(book_id, UUID))
        .first()
    )

    print("Book fetched from database")

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    pages = PagesDao.get_book_details(
        db,
        book_id
    )

    book_text = "\n".join(
        page.raw_content or ""
        for page in pages
    )

    if not book_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This book has no page content to summarize."
        )

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

    return {
        "message": "Book Created Successfully",
        "book_id": str(book.id),
        "title": book.title,
        "total_pages": book.total_pages
    }