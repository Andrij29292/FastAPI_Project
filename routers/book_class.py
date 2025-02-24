class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(
        self,
        book_id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_date: int,
    ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


SIGNS = {
    "id": lambda b: b.book_id,
    "rating": lambda b: b.rating,
    "pub_date": lambda b: b.published_date,
}


class Library:
    def __init__(self):
        self.__books: list[Book] = []

    def add_book(self, b: Book):
        b.book_id = self.__generate_book_id
        self.__books.append(b)
    
    def read_books(self) -> list[Book]:
        return self.__books

    def read_by(self, sign: str, field) -> list[Book]:
        if sign not in SIGNS:
            raise KeyError(f"Неправильний критерій пошуку: {sign}")

        return [b for b in self.__books if SIGNS[sign](b) == field]

    def delete_book(self, id: int):
        for i, b in enumerate(self.__books):
            if b.book_id == id:
                self.__books.pop(i)
                return

    def update_book(self, book_id: int, new_book: Book):
        for i, b in enumerate(self.__books):
            if b.book_id == book_id:
                new_book.book_id = book_id  # зберігаємо старий ID
                self.__books[i] = new_book
                return
        raise ValueError(f"Книга з ID {book_id} не знайдена")

    @property
    def __generate_book_id(self) -> int:
        return self.__books[-1].book_id + 1 if self.__books else 1
