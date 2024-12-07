from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import book
from app.utils.seeder import seed_books_from_json
#from app import models
#from app.configs.database import engine

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(book.router)

# Call the seeding function when the application starts
@app.on_event("startup")
async def startup():
    seed_books_from_json()  # Populate the database with books

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test/recommends/{prompt}")
def recommend_books_test(prompt: str):
    return {"message": prompt}
