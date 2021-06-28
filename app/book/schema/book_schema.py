from __future__ import annotations

from pydantic.main import BaseModel

from app.book.model.book_model import BookModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    is_creating: bool

    @staticmethod
    def from_book_model(book: BookModel) -> BookSchema:
        print(book)
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          is_creating=book.is_creating)
