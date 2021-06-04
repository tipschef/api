import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from app.database.service.database import Base


class RecipeModel(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    min_tier = Column(Integer, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    is_deleted = Column(Boolean, index=True, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    creator_id = Column(Integer, ForeignKey('user.id'), index=True)
    thumbnail_id = Column(Integer, ForeignKey('media.id'), index=True)
    video_id = Column(Integer, ForeignKey('media.id'), index=True)
    recipe_category_id = Column(Integer, ForeignKey('recipe_category.id'), index=True)
    recipe_cooking_type_id = Column(Integer, ForeignKey('recipe_cooking_type.id'), index=True)
    portion_number = Column(Integer, index=True)
    portion_unit = Column(String(255), index=True)
    preparation_hours = Column(Integer, index=True)
    preparation_minutes = Column(Integer, index=True)
    cooking_hours = Column(Integer, index=True)
    cooking_minutes = Column(Integer, index=True)
    resting_hours = Column(Integer, index=True)
    resting_minutes = Column(Integer, index=True)
    difficulty = Column(Integer, index=True)
    cost = Column(Integer, index=True)
