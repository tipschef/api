from sqlalchemy import Column, Integer, String, DateTime
import datetime

from app.database.service.database import Base


class IngredientModel(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
