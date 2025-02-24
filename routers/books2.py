from typing import Annotated, Optional
from fastapi import APIRouter, Body, Query, HTTPException, Path
from pydantic import BaseModel, Field
from .book_class import Book, Library
from starlette import status

books_router = APIRouter()
library = Library()

Short_text = Annotated[str, Field(max_length=256)]


class BookModel(BaseModel):
    book_id: Optional[int] = Field(description="is not needed on create", default=None)
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

    def to_book(self) -> Book:
        return Book(**self.model_dump())


def detail(_detail: str) -> dict[str, str]:
    return {"detail": _detail}


@books_router.get("/", status_code=status.HTTP_200_OK)
async def read_all_books():
    return library.read_books()


@books_router.get(
    "/read-by-published-date/{published_date}", status_code=status.HTTP_200_OK
)
async def read_book_by_published_date(published_date: int):
    books = library.read_by("pub_date", published_date)
    if not books:
        raise HTTPException(
            status_code=404, detail=f"No books published in {published_date} were found"
        )
    return books


@books_router.get("/read-by-rating", status_code=status.HTTP_200_OK)
async def read_book_by_rating(
    rating: int = Query(description="Book rating", le=10, gt=0)
):
    books = library.read_by("rating", rating)
    if not books:
        raise HTTPException(
            status_code=404, detail=f"No books with rating: {rating} were found"
        )
    return books


@books_router.get("/read-book-by-id/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    books = library.read_by("id", book_id)
    if not books:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    return books


@books_router.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookModel):
    book = new_book.to_book()
    library.add_book(book)
    return detail("book was created")


@books_router.put(
    "/update-book/{update_book_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def update_book(update_book_id: int = Path(gt=0), book: BookModel = Body(...)):
    try:
        library.update_book(update_book_id, book.to_book())
        return detail("book was updated")
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {update_book_id} not found, can't be updated",
        )


@books_router.delete(
    "/delete-book/{delete_book_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_book(delete_book_id: int = Path(gt=0)):
    try:
        library.delete_book(delete_book_id)
        return detail("book was deleted")
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {delete_book_id} not found, can't be deleted",
        )
