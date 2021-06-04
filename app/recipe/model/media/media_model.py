import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.database.service.database import Base


class MediaModel(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    media_category_id = Column(Integer, ForeignKey('media_category.id'), index=True)
