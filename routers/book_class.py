class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(
            self,
             book_id: int,
             title: str,
             author: str,
             description: str,
             rating: int
        ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
