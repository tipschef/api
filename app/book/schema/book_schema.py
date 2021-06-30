from __future__ import annotations

from typing import Optional

from pydantic.main import BaseModel

from app.book.model.book_model import BookModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    is_creating: bool
    path: Optional[str]
    number_of_recipe: Optional[int]

    @staticmethod
    def from_book_model(book: BookModel) -> BookSchema:
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          is_creating=book.is_creating)

    @staticmethod
    def from_book_model_and_number_of_recipe(book: BookModel, number_of_recipe: int) -> BookSchema:
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          path=book.path,
                          is_creating=book.is_creating,
                          number_of_recipe=number_of_recipe
                          )
