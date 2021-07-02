from dataclasses import dataclass
from typing import List, Tuple, Optional

from sqlalchemy.orm import Session

from app.book.model.book_model import BookModel
from app.book.model.book_recipe_model import BookRecipeModel
from app.book.schema.create_book_schema import CreateBookSchema


@dataclass
class BookRepository:

    @staticmethod
    def create_book(database: Session, book: CreateBookSchema, creator_id: int, u_id: str) -> BookModel:
        db_book = BookModel(title=book.name,
                            path='',
                            price_euro=book.price_euro,
                            description=book.description,
                            is_creating=True,
                            is_deleted=False,
                            creator_id=creator_id,
                            u_id=u_id)
        database.add(db_book)
        database.commit()
        database.refresh(db_book)
        return db_book

    @staticmethod
    def get_book_by_id(database: Session, book_id: int) -> Optional[BookModel]:
        return database.query(BookModel).filter(BookModel.id == book_id, BookModel.is_deleted.is_(False)).first()

    @staticmethod
    def get_book_by_recipe_id(database: Session, recipe_id: int) -> List[Tuple[BookModel, BookRecipeModel]]:
        return database.query(BookModel, BookRecipeModel)\
            .filter(BookModel.id == BookRecipeModel.book_id, BookModel.is_deleted.is_(False))\
            .filter(BookRecipeModel.recipe_id == recipe_id)\
            .all()

    @staticmethod
    def get_book_by_id_deleted_or_not(database: Session, book_id: int) -> BookModel:
        return database.query(BookModel).filter(BookModel.id == book_id).first()

    @staticmethod
    def delete_book_by_id(database: Session, book_id: int) -> None:
        database.query(BookModel).filter(BookModel.is_deleted.is_(False), BookModel.id == book_id).update(
            {BookModel.is_deleted: True})
        database.commit()

    @staticmethod
    def get_book_by_creator_id(database: Session, creator_id: int) -> List[BookModel]:
        return database.query(BookModel).filter(BookModel.creator_id == creator_id,
                                                BookModel.is_deleted.is_(False)).all()

    @staticmethod
    def update_book_by_id(database: Session, book_id: int, path: str) -> None:
        database.query(BookModel).filter(
            BookModel.is_deleted.is_(False), BookModel.id == book_id).update(
            {BookModel.path: path, BookModel.is_creating: False, BookModel.u_id: ''})
        database.commit()
