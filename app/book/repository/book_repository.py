from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.book.model.book_model import BookModel
from app.book.schema.create_book_schema import CreateBookSchema


@dataclass
class BookRepository:

    @staticmethod
    def create_book(database: Session, book: CreateBookSchema, creator_id: int) -> BookModel:
        db_book = BookModel(title=book.name,
                            path='',
                            price_euro=0,
                            description=book.description,
                            is_creating=True,
                            is_deleted=False,
                            creator_id=creator_id)
        database.add(db_book)
        database.commit()
        database.refresh(db_book)
        return db_book
