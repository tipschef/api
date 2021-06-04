from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.recipe.recipe_cooking_type_model import RecipeCookingTypeModel


@dataclass
class RecipeCookingTypeRepository:

    @staticmethod
    def create_recipe_cooking_type(database: Session, name: str) -> RecipeCookingTypeModel:
        db_recipe_cooking_type = RecipeCookingTypeModel(content=name, created_date=datetime.now())
        database.add(db_recipe_cooking_type)
        database.commit()
        database.refresh(db_recipe_cooking_type)
        return db_recipe_cooking_type

    @staticmethod
    def create_recipe_cooking_types(database: Session, recipe_cooking_types: List[str]) -> None:
        db_recipe_cooking_type_list = [
            RecipeCookingTypeModel(name=recipe_cooking_type, description='', created_date=datetime.now()) for recipe_cooking_type
            in recipe_cooking_types]
        database.bulk_save_objects(db_recipe_cooking_type_list)
        database.commit()

    @staticmethod
    def get_all_recipe_cooking_types(database: Session) -> List[RecipeCookingTypeModel]:
        return database.query(RecipeCookingTypeModel).filter(
            RecipeCookingTypeModel.is_deleted.is_(False)).all()
