from __future__ import annotations

from typing import Optional, List

from pydantic.main import BaseModel

from app.book.model.book_model import BookModel
from app.recipe.schema.recipe.recipe_simple_schema import RecipeSimpleSchema


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    is_creating: bool
    price_euro: Optional[float]
    path: Optional[str]
    number_of_recipe: Optional[int]
    recipes: Optional[List[RecipeSimpleSchema]]
    creator_id: Optional[int]

    @staticmethod
    def from_book_model(book: BookModel) -> BookSchema:
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          creator_id=book.creator_id,
                          is_creating=book.is_creating)

    @staticmethod
    def from_book_model_and_number_of_recipe(book: BookModel, number_of_recipe: int) -> BookSchema:
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          path=book.path,
                          is_creating=book.is_creating,
                          creator_id=book.creator_id,
                          number_of_recipe=number_of_recipe
                          )

    @staticmethod
    def from_book_model_and_recipes(book: BookModel, recipes: List[RecipeSimpleSchema]) -> BookSchema:
        return BookSchema(id=book.id,
                          title=book.title,
                          description=book.description,
                          path=book.path,
                          is_creating=book.is_creating,
                          price_euro=book.price_euro,
                          creator_id=book.creator_id,
                          recipes=recipes
                          )
