from sqlalchemy import Column, DateTime, Integer, ForeignKey
import datetime

from app.database.service.database import Base


class BookPurchaseModel(Base):
    __tablename__ = "book_purchase"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    book_id = Column(Integer, ForeignKey('book.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
