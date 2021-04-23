from sqlalchemy import Column, DateTime, Integer, ForeignKey, Float
import datetime

from app.database.service.database import Base


class RecipeIngredientsModel(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey('media.id'), index=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), index=True)
    ingredient_unit_id = Column(Integer, ForeignKey('ingredient_unit.id'), index=True)
    quantity = Column(Float, index=True)

    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
