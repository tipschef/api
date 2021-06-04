from dataclasses import dataclass
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.service.bucket_manager_service import get_bucket_manager_service
from app.recipe.exception.recipe_service_exceptions import RecipeIdNotFoundException, \
    CannotModifyOthersPeopleRecipeException, NotRecipeOwnerException
from app.recipe.repository.ingredient.ingredient_repository import IngredientRepository
from app.recipe.repository.ingredient.ingredient_unit_repository import IngredientUnitRepository
from app.recipe.repository.media.media_category_repository import MediaCategoryRepository
from app.recipe.repository.media.media_repository import MediaRepository
from app.recipe.repository.recipe.recipe_ingredients_repository import RecipeIngredientsRepository
from app.recipe.repository.recipe.recipe_medias_repository import RecipeMediasRepository
from app.recipe.repository.recipe.recipe_repository import RecipeRepository
from app.recipe.repository.step.step_repository import StepRepository
from app.recipe.schema.media.media_base_schema import MediaBaseSchema
from app.recipe.schema.media.media_category_schema import MediaCategorySchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe.recipe_schema import RecipeSchema
from app.recipe.schema.step.step_schema import StepSchema
from app.user.schema.user_schema import UserSchema


@dataclass
class RecipeService:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema) -> int:
        # create recipe
        recipe_created = RecipeRepository.create_recipe(database, recipe)
        # create steps
        StepRepository.create_steps(database, recipe.steps, recipe_created.id)

        for ingredient_bloc in recipe.ingredients:
            ingredient = IngredientRepository.get_ingredient_by_name(database, ingredient_bloc.ingredient_name)
            if ingredient is None:
                ingredient = IngredientRepository.create_ingredient(database, ingredient_bloc.ingredient_name)

            ingredient_unit = IngredientUnitRepository.get_ingredient_unit_by_name(database, ingredient_bloc.ingredient_unit)
            if ingredient_unit is None:
                ingredient_unit = IngredientUnitRepository.create_ingredient_unit(database, ingredient_bloc.ingredient_unit)

            RecipeIngredientsRepository.create_recipe_ingredients(database, recipe_created.id, ingredient.id, ingredient_unit.id, ingredient_bloc.quantity)
        return recipe_created.id

    @staticmethod
    def get_all_recipe_for_specific_user(database: Session, user_id: int) -> List[RecipeResponseSchema]:
        recipes_list_response = []
        recipes_list = RecipeRepository.get_all_recipe_for_user(database, user_id)
        for recipe in recipes_list:
            video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
            thumbnail_media = MediaSchema.from_media_model(
                MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
            steps = [StepSchema.from_step_model(step) for step in
                     StepRepository.get_steps_by_recipe_id(database, recipe.id)]
            recipes_list_response.append(
                RecipeResponseSchema.from_recipe_model(recipe, steps=steps, thumbnail=thumbnail_media,
                                                       video=video_media))
        return recipes_list_response

    @staticmethod
    def get_a_recipe_by_id(database: Session, recipe_id: int) -> RecipeResponseSchema:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        if recipe is None:
            raise RecipeIdNotFoundException()
        video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
        thumbnail_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
        steps = [StepSchema.from_step_model(step) for step in
                 StepRepository.get_steps_by_recipe_id(database, recipe_id)]
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
        _ = [StepRepository.delete_step_by_id(database, step.id) for step in
             StepRepository.get_steps_by_recipe_id(database, recipe_id)]
        RecipeRepository.delete_recipe_by_id(database, recipe_id)
        return True

    @staticmethod
    def update_a_recipe_by_id(database: Session, recipe_id: int, current_user: UserSchema,
                              recipe: RecipeResponseSchema) -> bool:
        recipe_to_update = recipe
        recipe_from_db = RecipeRepository.get_recipe_by_id(database, recipe_id)

        if recipe_from_db is None:
            raise RecipeIdNotFoundException()
        if recipe_from_db.creator_id != current_user.id:
            raise CannotModifyOthersPeopleRecipeException()

        # update recipe
        RecipeRepository.update_recipe_by_id(database, recipe_id, recipe_to_update)

        _ = [StepRepository.delete_step_by_id(database, step.id) for step in
             StepRepository.get_steps_by_recipe_id(database, recipe_id)]

        StepRepository.create_steps(database, recipe.steps, recipe_id)

        return True

    @staticmethod
    def get_my_wall(database: Session, user: UserSchema) -> List[RecipeResponseSchema]:
        recipes = []
        recipes_list = RecipeRepository.get_followed_recipes(database, user.id)
        for recipe in recipes_list:
            video_media = MediaSchema.from_media_model(MediaRepository.get_media_by_id(database, recipe.video_id))
            thumbnail_media = MediaSchema.from_media_model(
                MediaRepository.get_media_by_id(database, recipe.thumbnail_id))
            steps = [StepSchema.from_step_model(step) for step in
                     StepRepository.get_steps_by_recipe_id(database, recipe.id)]
            recipes.append(RecipeResponseSchema.from_recipe_model(recipe, steps=steps, thumbnail=thumbnail_media,
                                                                  video=video_media))
        return recipes

    @staticmethod
    def add_media_to_recipe(database: Session, creator_id: int, recipe_id: int, medias: List[UploadFile]) -> List[MediaSchema]:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        created_media_ids = []
        created_medias = []
        if recipe is None:
            raise RecipeIdNotFoundException()
        if recipe.creator_id != creator_id:
            raise NotRecipeOwnerException()

        for media in medias:
            media_category = MediaCategoryRepository.get_media_category_by_name(database, media.content_type.split('/')[0])
            if media_category is None:
                media_category = MediaCategoryRepository.create_media_category(database, MediaCategorySchema(name=media.content_type.split('/')[0], description=media.content_type.split('/')[0]))
            media_schema = MediaBaseSchema(path='temp', media_category_id=media_category.id)
            created_media = MediaRepository.create_media(database, media_schema)
            filename = get_bucket_manager_service().save_file(f'{creator_id}/{recipe_id}/{created_media.id}_{media.filename}', media.file)
            created_media.path = filename
            MediaRepository.update_media_by_id(database, created_media.id, filename)
            created_media_ids.append(created_media.id)

            created_medias.append(MediaSchema.from_media_model(created_media))

        RecipeMediasRepository.create_medias(database, created_media_ids, recipe_id)
        return created_medias
