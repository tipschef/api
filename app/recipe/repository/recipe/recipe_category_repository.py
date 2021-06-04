from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.recipe.recipe_category_model import RecipeCategoryModel


@dataclass
class RecipeCategoryRepository:

    @staticmethod
    def create_recipe_category(database: Session, name: str) -> RecipeCategoryModel:
        db_recipe_category = RecipeCategoryModel(content=name, created_date=datetime.now())
        database.add(db_recipe_category)
        database.commit()
        database.refresh(db_recipe_category)
        return db_recipe_category

    @staticmethod
    def create_recipe_categories(database: Session, recipe_categories: List[str]) -> None:
        db_recipe_category_list = [
            RecipeCategoryModel(name=recipe_category, description='', created_date=datetime.now()) for recipe_category
            in recipe_categories]
        database.bulk_save_objects(db_recipe_category_list)
        database.commit()

    @staticmethod
    def get_all_recipe_categories(database: Session) -> List[RecipeCategoryModel]:
        return database.query(RecipeCategoryModel).filter(
            RecipeCategoryModel.is_deleted.is_(False)).all()
