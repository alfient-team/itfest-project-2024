from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.configs.database import Base
from app.configs.database import engine


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    image_link = Column(String, nullable=False)

Base.metadata.create_all(engine)
