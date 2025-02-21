from typing import Annotated, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from .book_class import Book

books_router = APIRouter(prefix="/books", tags=["Book"])

Short_text = Annotated[str, Field(max_length=256)]

class BookModel(BaseModel):
    book_id: Optional[int] = Field(description='is not needed on create', default=None)
    title: Short_text
    author: Short_text
    description: Short_text
    rating: int = Field(gt=0, le=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Shulla Andrew",
                "description": "A new description of book",
                "rating": 5,
            }
        }
    }

    def conversion_into_book(self) -> Book:
        return Book(**self.model_dump())


BOOKS_DATABASE: list[Book] = [
    Book(book_id=1, title="1984", author="George Orwell", description="Dystopian novel about totalitarianism.", rating=9),
    Book(book_id=2, title="To Kill a Mockingbird", author="Harper Lee", description="Story of racial injustice in America.", rating=10),
    Book(book_id=3, title="The Great Gatsby", author="F. Scott Fitzgerald", description="A critique of the American Dream.", rating=8),
    Book(book_id=4, title="Moby-Dick", author="Herman Melville", description="A sailor’s narrative about the white whale.", rating=7),
    Book(book_id=5, title="Pride and Prejudice", author="Jane Austen", description="Romantic novel about manners and marriage.", rating=9)
]

@books_router.get("")
async def read_all_books():
    return BOOKS_DATABASE

@books_router.get("/{book_id}")
async def get_book_by_id(book_id: int):
    return (b for b in BOOKS_DATABASE if b.book_id == book_id)

@books_router.get("/")
async def read_book_by_rating(rating: int=Query(..., gt=0, le=10)):
    response = (b for b in BOOKS_DATABASE if b.rating == rating)

    if sum(1 for _ in response) == 0:
        return detail(f"no books with a rating of {rating} were found")

    return (b for b in BOOKS_DATABASE if b.rating == rating)

@books_router.post("/create-book")
async def create_book(new_book: BookModel):
    BOOKS_DATABASE.append(generate_book_id(new_book.conversion_into_book()))

    return detail("book was created")


def generate_book_id(b: Book):
    b.book_id = BOOKS_DATABASE[-1].book_id + 1 if len(BOOKS_DATABASE) > 0 else 1
    return b

@books_router.put("/update-book/{update_book_id}")
async def update_book(update_book_id: int, book: BookModel):
    for i in range(len(BOOKS_DATABASE)):
        if BOOKS_DATABASE[i].book_id == update_book_id:
            book.book_id = update_book_id
            BOOKS_DATABASE[i] = book.conversion_into_book()
            return detail("book was updated")


    return detail(f"book with id {book.book_id} were not found, can`t be updated")


def detail(_detail: str) -> dict[str, str]:
    return {"detail": _detail}



