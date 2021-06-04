import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database.service.database import Base


class RecipeCategoryModel(Base):
    __tablename__ = 'recipe_category'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
