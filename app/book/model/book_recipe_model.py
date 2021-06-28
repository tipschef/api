import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String

from app.database.service.database import Base


class BookRecipeModel(Base):
    __tablename__ = "book_recipe"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), index=True)
    book_id = Column(Integer, ForeignKey('book.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
