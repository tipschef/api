import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.database.service.database import Base


class RecipeMediasModel(Base):
    __tablename__ = "recipe_medias"

    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey('media.id'), index=True)
    recipe_id = Column(Integer, ForeignKey('recipe.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
