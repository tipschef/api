from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.book.model.book_recipe_model import BookRecipeModel


@dataclass
class BookRecipeRepository:

    @staticmethod
    def create_book_recipe(database: Session, book_id: int, recipe_id: int) -> BookRecipeModel:
        db_recipe_book = BookRecipeModel(book_id=book_id, recipe_id=recipe_id)
        database.add(db_recipe_book)
        database.commit()
        database.refresh(db_recipe_book)
        return db_recipe_book

    @staticmethod
    def get_number_recipe_by_book(database: Session, book_id: int) -> int:
        return database.query(BookRecipeModel).filter(BookRecipeModel.book_id == book_id).count()

