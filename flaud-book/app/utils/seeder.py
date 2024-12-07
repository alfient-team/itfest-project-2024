import json
import os
from app.models.book import Book
from app.configs.database import SessionLocal
from sqlalchemy.orm import Session

# Function to load and seed the database
def seed_books_from_json():
    # Get the absolute path of the data.json file
    data_file_path = os.path.join(os.path.dirname(__file__), 'data.json')

    # Load data from data.json file
    with open(data_file_path, "r") as f:
        data = json.load(f)
    
    db: Session = SessionLocal()  # Creating a session

    for book_id, book_data in data.items():
        # Check if the book already exists by its id
        existing_book = db.query(Book).filter(Book.id == book_id).first()

        # If book does not exist, insert it into the database
        if not existing_book:
            new_book = Book(
                id=book_id,
                title=book_data["title"],
                author=book_data["author"],
                image_link=book_data["image_link"]
            )
            db.add(new_book)
            db.commit()  # Commit the transaction
            db.refresh(new_book)  # Retrieve the created post

            print(f"Book with ID {book_id} added to the database.")
        else:
            print(f"Book with ID {book_id} already exists in the database.")
    
    db.close()  # Close the database session after all operations
