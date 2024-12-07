from pydantic import BaseModel
from typing import List


class IBookBase(BaseModel):
    title: str
    author: str
    image_link: str


class IBook(IBookBase):
    id: int

    class Config:
        from_attributes = True  # Ensure Pydantic can handle SQLAlchemy models

class ICreateBook(IBookBase):
    pass

class IBookResponse(BaseModel):
    id: int
    book: IBookBase
    generated_summary: str
    generated_reason: str

    class Config:
        from_attributes = True


class IBookListResponse(BaseModel):
    book_list: List[IBookResponse]

    class Config:
        from_attributes = True
