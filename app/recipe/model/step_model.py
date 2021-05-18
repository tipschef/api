import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.database.service.database import Base


class StepModel(Base):
    __tablename__ = "step"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
