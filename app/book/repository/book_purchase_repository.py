from dataclasses import dataclass
from typing import List, Tuple, Optional

from sqlalchemy.orm import Session

from app.book.model.book_model import BookModel
from app.book.model.book_purchase_model import BookPurchaseModel


@dataclass
class BookPurchaseRepository:

    @staticmethod
    def create_purchase(database: Session, book_id: int, user_id: int) -> BookPurchaseModel:
        db_purchase = BookPurchaseModel(book_id=book_id, user_id=user_id)
        database.add(db_purchase)
        database.commit()
        database.refresh(db_purchase)
        return db_purchase

    @staticmethod
    def get_purchase_by_user_id(database: Session, user_id: int) -> List[Tuple[BookPurchaseModel, BookModel]]:
        return database.query(BookPurchaseModel, BookModel) \
            .join(BookModel, BookModel.id == BookPurchaseModel.book_id) \
            .filter(BookPurchaseModel.user_id == user_id) \
            .order_by(BookPurchaseModel.created_date.desc()) \
            .all()

    @staticmethod
    def find_purchase_by_user_id_and_book_id(database: Session, user_id: int, book_id) -> Optional[BookPurchaseModel]:
        return database.query(BookPurchaseModel) \
            .filter(BookPurchaseModel.user_id == user_id) \
            .filter(BookPurchaseModel.book_id == book_id) \
            .first()
