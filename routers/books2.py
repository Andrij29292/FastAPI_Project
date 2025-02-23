from typing import Annotated, Optional

from fastapi import APIRouter, Body, Query, HTTPException, Path
from pydantic import BaseModel, Field
from .book_class import Book

books_router = APIRouter()

Short_text = Annotated[str, Field(max_length=256)]

class BookModel(BaseModel):
    book_id: Optional[int] = Field(description='is not needed on create', default=None)
    title: Short_text
    author: Short_text
    description: Short_text
    rating: int = Field(gt=0, le=10)
    published_date: int = Field(le=2025)


    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Shulla Andrew",
                "description": "A new description of book",
                "rating": 5,
                "published_date": 2024,
            }
        }
    }

    def conversion_into_book(self) -> Book:
        return Book(**self.model_dump())

BOOKS_DATABASE: list[Book] = [
    Book(book_id=1, title="1984", author="George Orwell", description="Dystopian novel about totalitarianism.", rating=9, published_date=1949),
    Book(book_id=2, title="To Kill a Mockingbird", author="Harper Lee", description="Story of racial injustice in America.", rating=10, published_date=1960),
    Book(book_id=3, title="The Great Gatsby", author="F. Scott Fitzgerald", description="A critique of the American Dream.", rating=8, published_date=1925),
    Book(book_id=4, title="Moby-Dick", author="Herman Melville", description="A sailor’s narrative about the white whale.", rating=7, published_date=1851),
    Book(book_id=5, title="Pride and Prejudice", author="Jane Austen", description="Romantic novel about manners and marriage.", rating=9, published_date=1813)
]

def detail(_detail: str) -> dict[str, str]:
    return {"detail": _detail}

def generate_book_id(b: Book):
    b.book_id = BOOKS_DATABASE[-1].book_id + 1 if len(BOOKS_DATABASE) > 0 else 1
    return b

@books_router.get("")
async def read_all_books():
    return BOOKS_DATABASE



@books_router.get("/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    return (b for b in BOOKS_DATABASE if b.book_id == book_id)



@books_router.get("/read-by-published-date/{published_date}")
async def read_book_by_published_date(published_date: int):
    response = [b for b in BOOKS_DATABASE if b.published_date == published_date]

    if not response:
        raise HTTPException(status_code=404, detail=f"No books published in {published_date} were found")

    return response



@books_router.get("/read-by-rating/")
async def read_book_by_rating(rating: int=Query(..., gt=0, le=10)):
    response = [b for b in BOOKS_DATABASE if b.rating == rating]

    if not response:
        raise HTTPException(status_code=404, detail=f"No books with rating: {rating} were found")

    return response



@books_router.post("/create-book")
async def create_book(new_book: BookModel):
    BOOKS_DATABASE.append(generate_book_id(new_book.conversion_into_book()))

    return detail("book was created")



@books_router.put("/update-book/{update_book_id}")
async def update_book(update_book_id: int = Path(gt=0), book: BookModel = Body(...)):
    for i in range(len(BOOKS_DATABASE)):
        if BOOKS_DATABASE[i].book_id == update_book_id:
            book.book_id = update_book_id
            BOOKS_DATABASE[i] = book.conversion_into_book()
            return detail("book was updated")


    return detail(f"book with id {update_book_id} were not found, can`t be updated")



@books_router.delete("/delete-book/{delete_book_id}")
async def delete_book(delete_book_id: int = Path(gt=0)):
    for i in range(len(BOOKS_DATABASE)):
        if BOOKS_DATABASE[i].book_id == delete_book_id:
            BOOKS_DATABASE.pop(i)
            return detail(f"book was deleted")

    return detail(f"book with id {delete_book_id} were not found, can`t be deleted")



