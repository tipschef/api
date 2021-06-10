from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.repository.recipe.recipe_category_repository import RecipeCategoryRepository
from app.recipe.schema.recipe.recipe_category_schema import RecipeCategorySchema, RecipeCategoryResponseSchema


@dataclass
class RecipeCategoryService:
    @staticmethod
    def get_all_recipe_categories(database: Session) -> List[RecipeCategoryResponseSchema]:
        recipe_category_list = RecipeCategoryRepository.get_all_recipe_categories(database)
        return [RecipeCategoryResponseSchema.from_recipe_category_model(recipe_category) for recipe_category in recipe_category_list]