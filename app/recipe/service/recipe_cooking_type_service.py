from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.repository.recipe.recipe_cooking_type_repository import RecipeCookingTypeRepository
from app.recipe.schema.recipe.recipe_cooking_type_schema import RecipeCookingTypeSchema, RecipeCookingTypeResponseSchema


@dataclass
class RecipeCookingTypeService:
    @staticmethod
    def get_all_recipe_categories(database: Session) -> List[RecipeCookingTypeResponseSchema]:
        recipe_cooking_type_list = RecipeCookingTypeRepository.get_all_recipe_cooking_types(database)
        return [RecipeCookingTypeResponseSchema.from_recipe_cooking_type_model(recipe_cooking_type) for recipe_cooking_type in recipe_cooking_type_list]