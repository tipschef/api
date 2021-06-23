import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean

from app.database.service.database import Base


class CommentModel(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
