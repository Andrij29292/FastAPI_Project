import uvicorn
from fastapi import FastAPI
from routers.books2 import books_router

app = FastAPI(title="Books Project")

app.include_router(books_router, prefix="/books", tags=["Book"])


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
