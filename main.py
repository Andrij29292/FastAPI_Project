from fastapi import FastAPI
from routers.books2 import books_router
app = FastAPI(title="Books Project")

app.include_router(books_router)


