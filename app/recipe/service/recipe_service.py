from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.repository.recipe_repository import RecipeRepository
from app.recipe.schema.recipe_schema import RecipeSchema


@dataclass
class RecipeService:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema):
        print(recipe)
        return RecipeRepository.create_recipe(database, recipe)
