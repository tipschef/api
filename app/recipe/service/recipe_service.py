from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.repository.media_repository import MediaRepository
from app.recipe.repository.recipe_repository import RecipeRepository
from app.recipe.repository.step_repository import StepRepository
from app.recipe.schema.recipe_schema import RecipeSchema


@dataclass
class RecipeService:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema) -> RecipeSchema:
        # create video
        video_model = MediaRepository.create_media(database, recipe.video)
        # create thumbnail
        thumbnail_model = MediaRepository.create_media(database, recipe.thumbnail)
        recipe = RecipeRepository.create_recipe(database, recipe, video_model.id, thumbnail_model.id)
        # create steps
        StepRepository.create_steps(database, recipe.steps, recipe.id)

        return recipe

    @staticmethod
    def get_all_recipe_for_specific_user(database: Session, user_id: int):
        recipes_list = RecipeRepository.get_all_recipe_for_user(database, user_id)
        return [RecipeSchema.from_recipe_model(recipe) for recipe in recipes_list]
