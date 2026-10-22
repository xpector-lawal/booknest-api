
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Book, BookCreate, BookResponse


# Create database tables when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="BookNest Digital Library API",
    description=(
        "A RESTful backend for managing a digital library's "
        "book inventory using FastAPI and PostgreSQL."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def home():
    return {
        "name": "BookNest Digital Library API",
        "message": "Welcome to BookNest.",
        "docs": "/docs",
    }


@app.post(
    "/books",
    response_model=dict[str, str],
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db),
):
    new_book = Book(**book_data.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return {"message": "Book added"}


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    statement = select(Book).order_by(Book.id)
    books = db.scalars(statement).all()

    return books


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} was not found.",
        )

    return book
