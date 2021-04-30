import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database.service.database import Base


class MediaCategoryModel(Base):
    __tablename__ = "media_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
