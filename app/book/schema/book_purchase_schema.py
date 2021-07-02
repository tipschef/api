from datetime import datetime

from pydantic import BaseModel

from app.book.model.book_model import BookModel
from app.book.model.book_purchase_model import BookPurchaseModel
from app.user.model.user_model import UserModel


class BookPurchaseSchema(BaseModel):
    book_id: int
    buy_date: datetime
    title: str
    path: str
    price_euro: float
    creator: str

    @staticmethod
    def from_model(book_purchase_model: BookPurchaseModel, book_model: BookModel, user_model: UserModel):
        return BookPurchaseSchema(buy_date=book_purchase_model.created_date,
                                  title=book_model.title,
                                  path=book_model.path,
                                  price_euro=book_model.price_euro,
                                  creator=user_model.username,
                                  book_id=book_purchase_model.book_id)
