import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float

from app.database.service.database import Base


class BookModel(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    path = Column(String(255), index=True)
    price_euro = Column(Float, unique=True, index=True)
    description = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    creator_id = Column(Integer, ForeignKey('user.id'), index=True)
