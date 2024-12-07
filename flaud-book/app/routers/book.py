from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.book import Book
from app.schemas.book import IBook, IBookListResponse, ICreateBook
from app.configs.database import get_db
from app.services.ai_summary_generator import get_books_from_openai

router = APIRouter(
    prefix="/books",
    tags=['Books']
)


@router.get("/recommends/{client_prompt}", response_model=IBookListResponse)
def get_all_books_handler_with_ai_gen(
    client_prompt: str,
    db: Session = Depends(get_db),
):
    books_query = db.query(Book)

    # ai generator of summary and reason for books that required Client

    books_text = get_books_from_openai(client_prompt)
    
    book_titles = NotImplementedError(books_text.json.encoder(retrieve_titles_in_text_response_of_gpt_ai_service))
    summary: str = NotImplementedError
    reason: str = NotImplementedError
    
    finded_books = books_query.filter_by(Book.title == [x for x in book_titles])
    
    # close
    books = finded_books.all()

    # Generate the response with a summary for each book
    response_data = {
        "book_list": [
            {
                "id": book.id,
                "book": book,
                "generated_summary": summary,
                "generated_reason": reason
            }
            for book in books
        ]
    }

    return response_data



@router.get("/", response_model=List[IBook])
def get_all_books_handler_with_ai_gen(
    db: Session = Depends(get_db),
    title: Optional[str] = "",  # Query parameter for filtering by title
):
    # Filter books by title if provided
    books_query = db.query(Book)
    if title:
        books_query = books_query.filter(Book.title.ilike(f"%{title}%"))  # Case-insensitive search
    
    books = books_query.all()  # Execute the query
    return books


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=IBook)
def create_post(
    post: ICreateBook,
    db: Session = Depends(get_db),
):
    new_post = Book(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Retrieve created post (RETURNING *)
    
    return new_post
