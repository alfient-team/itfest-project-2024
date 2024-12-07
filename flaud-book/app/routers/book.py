from json import JSONDecodeError
import json
from fastapi import Response, status, HTTPException, Depends, APIRouter
import requests
from sqlalchemy import func
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
    """
    Handles book recommendations with AI-generated summaries and reasons.
    """
    books_query = db.query(Book)

    try:
        # Fetch book recommendations from OpenAI
        books_text = get_books_from_openai(client_prompt)

        # Clean and parse the JSON response
        if books_text.startswith("```json"):
            books_text = books_text[7:]
        if books_text.endswith("```"):
            books_text = books_text[:-3]
        books_json = json.loads(books_text)

    except JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to decode AI-generated book recommendations."
        )
    except requests.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI API error: {str(e)}"
        )

    # Extract titles from AI response
    book_titles = [book_data.get("title") for book_data in books_json.values()]

    if not book_titles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No books were recommended by the AI."
        )

    # Query the database for matching books (case-insensitive)
    # TODO: smart searcher
    finded_books = books_query.filter(
        func.lower(Book.title).in_([title.lower() for title in book_titles])
    ).all()

    # Debug logging
    print("AI Titles:", book_titles)
    print("Database Matched Books:", [book.title for book in finded_books])

    # Prepare the response
    book_recommendations = []
    for db_book in finded_books:
        ai_data = next(
            (data for data in books_json.values() if data.get("title") == db_book.title),
            None
        )
        if ai_data:
            book_recommendations.append({
                "id": db_book.id,
                "book": db_book,
                "generated_summary": ai_data.get("summary", "Summary not available."),
                "generated_reason": ai_data.get("reason", "Reason not available.")
            })

    return {
        "book_list": book_recommendations
    }


#@router.get("/recommends/{client_prompt}", response_model=IBookListResponse)
#def get_all_books_handler_with_ai_gen(
#    client_prompt: str,
#    db: Session = Depends(get_db),
#):
#    books_query = db.query(Book)

#    # ai generator of summary and reason for books that required Client

#    books_text = get_books_from_openai(client_prompt)
    
#    book_titles = NotImplementedError(books_text.json.encoder(retrieve_titles_in_text_response_of_gpt_ai_service))
#    summary: str = NotImplementedError
#    reason: str = NotImplementedError
    
#    finded_books = books_query.filter_by(Book.title == [x for x in book_titles])
    
#    # close
#    books = finded_books.all()

#    # Generate the response with a summary for each book
#    response_data = {
#        "book_list": [
#            {
#                "id": book.id,
#                "book": book,
#                "generated_summary": summary,
#                "generated_reason": reason
#            }
#            for book in books
#        ]
#    }

#    return response_data



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
