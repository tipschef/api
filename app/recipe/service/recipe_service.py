from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.exception.recipe_service_exceptions import RecipeIdNotFoundException, \
    CannotModifyOthersPeopleRecipeException
from app.recipe.repository.media_repository import MediaRepository
from app.recipe.repository.recipe_repository import RecipeRepository
from app.recipe.repository.step_repository import StepRepository
from app.recipe.schema.media_schema import MediaSchema
from app.recipe.schema.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe_schema import RecipeSchema
from app.recipe.schema.step_schema import StepSchema
from app.user.schema.user_schema import UserSchema


@dataclass
class RecipeService:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema) -> int:
        # create video
        video_model = MediaRepository.create_media(database, recipe.video)
        # create thumbnail
        thumbnail_model = MediaRepository.create_media(database, recipe.thumbnail)
        # create recipe
        recipe_created = RecipeRepository.create_recipe(database, recipe, video_model.id, thumbnail_model.id)
        # create steps
        StepRepository.create_steps(database, recipe.steps, recipe_created.id)
        return recipe_created.id

    @staticmethod
    def get_all_recipe_for_specific_user(database: Session, user_id: int) -> List[RecipeResponseSchema]:
        recipes_list_response = []
        recipes_list = RecipeRepository.get_all_recipe_for_user(database, user_id)
        for recipe in recipes_list:
            video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
            thumbnail_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
            steps = [StepSchema.from_step_model(step) for step in StepRepository.get_steps_by_recipe_id(database, recipe.id)]
            recipes_list_response.append(RecipeResponseSchema.from_recipe_model(recipe, steps=steps, thumbnail=thumbnail_media, video=video_media))
        return recipes_list_response

    @staticmethod
    def get_a_recipe_by_id(database: Session, recipe_id: int) -> RecipeResponseSchema:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        if recipe is None:
            raise RecipeIdNotFoundException()
        video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
        thumbnail_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
        steps = [StepSchema.from_step_model(step) for step in StepRepository.get_steps_by_recipe_id(database, recipe_id)]
        return RecipeResponseSchema.from_recipe_model(recipe, steps=steps, thumbnail=thumbnail_media, video=video_media)

    @staticmethod
    def delete_a_recipe_by_id(database: Session, recipe_id: int, current_user: UserSchema) -> bool:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        if recipe is None:
            raise RecipeIdNotFoundException()
        if recipe.creator_id != current_user.id:
            raise CannotModifyOthersPeopleRecipeException()
        MediaRepository.delete_media_by_id(database, recipe.video_id)
        MediaRepository.delete_media_by_id(database, recipe.thumbnail_id)
        _ = [StepRepository.delete_step_by_id(database, step.id) for step in StepRepository.get_steps_by_recipe_id(database, recipe_id)]
        RecipeRepository.delete_recipe_by_id(database, recipe_id)
        return True

    @staticmethod
    def update_a_recipe_by_id(database: Session, recipe_id: int, current_user: UserSchema, recipe: RecipeResponseSchema) -> bool:
        recipe_to_update = recipe
        recipe_from_db = RecipeRepository.get_recipe_by_id(database, recipe_id)

        if recipe_from_db is None:
            raise RecipeIdNotFoundException()
        if recipe_from_db.creator_id != current_user.id:
            raise CannotModifyOthersPeopleRecipeException()

        # update thumbnail
        if recipe.thumbnail.id is not None and recipe.thumbnail.id == recipe_from_db.thumbnail_id:
            MediaRepository.update_media_by_id(database, recipe_from_db.thumbnail_id, recipe.thumbnail.path)
        else:
            MediaRepository.delete_media_by_id(database, recipe_from_db.thumbnail_id)
            recipe_to_update.thumbnail.id = MediaRepository.create_media(database, recipe.thumbnail).id
        # update video
        if recipe.video.id is not None and recipe.video.id == recipe_from_db.video_id:
            MediaRepository.update_media_by_id(database, recipe_from_db.video_id, recipe.video.path)
        else:
            MediaRepository.delete_media_by_id(database, recipe_from_db.video_id)
            recipe_to_update.video.id = MediaRepository.create_media(database, recipe.video).id

        # update recipe
        RecipeRepository.update_recipe_by_id(database, recipe_id, recipe_to_update)

        _ = [StepRepository.delete_step_by_id(database, step.id) for step in StepRepository.get_steps_by_recipe_id(database, recipe_id)]

        StepRepository.create_steps(database, recipe.steps, recipe_id)

        return True

    @staticmethod
    def get_my_wall(database: Session, user: UserSchema) -> List[RecipeResponseSchema]:
        recipes = []
        recipes_list = RecipeRepository.get_followed_recipes(database, user.id)
        for recipe in recipes_list:
            video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
            thumbnail_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
            steps = [StepSchema.from_step_model(step) for step in StepRepository.get_steps_by_recipe_id(database, recipe.id)]
            recipes.append(RecipeResponseSchema.from_recipe_model(recipe, steps=steps, thumbnail=thumbnail_media, video=video_media))
        return recipes
