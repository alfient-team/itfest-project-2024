from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.book import Book
from app.schemas.book import IBook, IBookListResponse
from app.configs.database import get_db

router = APIRouter(
    prefix="/books",
    tags=['Books']
)

@router.get("/", response_model=List[IBook])
def get_all_books_handler(
    db: Session = Depends(get_db), 
    title: Optional[str] = "",  # Query parameter for filtering by title
):
    # Filter books by title if provided
    books_query = db.query(Book)
    if title:
        books_query = books_query.filter(Book.title.ilike(f"%{title}%"))  # Case-insensitive search
    
    books = books_query.all()  # Execute the query
    return books


#@router.get("/recommeds/{summary_prompt}", response_model=List[IBookListResponse])
#def get_all_books_with_generated_summary_handler(
#    summary_prompt: str,
#    db: Session = Depends(get_db),
#):
#    books_query = db.query(Book)
    
#    book = books_query.all()
    
#    summary = f"some generated summary for specific book: {summary_prompt=}"
    
#    response_dict = {
#        "books": book,
#        "generated_summary": summary,  # generated book summary per one book
#    }
    
#    return response_dict  # responde with multiple books and with generated summary below for each

@router.get("/recommends/{summary_prompt}", response_model=IBookListResponse)
def get_all_books_handler(
    summary_prompt: str,
    db: Session = Depends(get_db),
):
    books_query = db.query(Book)

    books = books_query.all()

    # Generate the response with a summary for each book
    response_data = {
        "book_list": [
            {
                "id": book.id,
                "book": book,
                "generated_summary": f"Generated summary for book titled '{summary_prompt=}'"
            }
            for book in books
        ]
    }

    return response_data

