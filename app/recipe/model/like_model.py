import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.database.service.database import Base


class LikeModel(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
