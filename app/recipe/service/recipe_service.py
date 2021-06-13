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
from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.media.media_base_schema import MediaBaseSchema
from app.recipe.schema.media.media_category_schema import MediaCategorySchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe.recipe_response_extended_schema import RecipeResponseExtendedSchema
from app.recipe.schema.recipe.recipe_schema import RecipeSchema
from app.recipe.schema.step.step_schema import StepSchema
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_schema import UserSchema


@dataclass
class RecipeService:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeBaseSchema, creator_id: int) -> int:
        # create recipe
        recipe_created = RecipeRepository.create_recipe(database, recipe, creator_id)
        # create steps
        StepRepository.create_steps(database, recipe.steps, recipe_created.id)

        for ingredient_bloc in recipe.ingredients:
            ingredient = IngredientRepository.get_ingredient_by_name(database, ingredient_bloc.ingredient_name)
            if ingredient is None:
                ingredient = IngredientRepository.create_ingredient(database, ingredient_bloc.ingredient_name)

            ingredient_unit = IngredientUnitRepository.get_ingredient_unit_by_name(database,
                                                                                   ingredient_bloc.ingredient_unit)
            if ingredient_unit is None:
                ingredient_unit = IngredientUnitRepository.create_ingredient_unit(database,
                                                                                  ingredient_bloc.ingredient_unit)

            RecipeIngredientsRepository.create_recipe_ingredients(database, recipe_created.id, ingredient.id,
                                                                  ingredient_unit.id, ingredient_bloc.quantity)
        return recipe_created.id

    @staticmethod
    def get_all_recipe_for_specific_user(database: Session, current_user: UserSchema, asking_username: str) -> List[RecipeResponseExtendedSchema]:
        asking_user = UserRepository.get_user_by_username(asking_username)
        subscription = SubscriptionRepository.get_subscription(database, asking_user.id, current_user.id)

        recipes_list_response = []
        recipes_list = RecipeRepository.get_all_recipe_for_user(database, asking_user.id)
        for recipe in recipes_list:
            steps = [StepSchema.from_step_model(step) for step in
                     StepRepository.get_steps_by_recipe_id(database, recipe.id)]

            ingredients = [IngredientBaseSchema.from_ingredient_tuple(ingredient[0], ingredient[1], ingredient[2]) for
                           ingredient in
                           RecipeIngredientsRepository.get_recipe_ingredients_by_recipe_id(database, recipe.id)]

            medias = [MediaSchema.from_media_model(media[1]) for
                      media in RecipeMediasRepository.get_all_recipe_medias_data_by_recipe_id(database, recipe.id)]

            can_be_seen = current_user.id == asking_user.id or recipe.min_tier == 0 or (subscription is not None and recipe.min_tier <= subscription.tier)
            recipes_list_response.append(
                RecipeResponseExtendedSchema.from_recipe_models_seen(recipe, steps=steps, ingredients=ingredients, medias=medias, can_be_seen=can_be_seen))
        return recipes_list_response

    @staticmethod
    def get_a_recipe_by_id(database: Session, recipe_id: int) -> RecipeResponseSchema:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        if recipe is None:
            raise RecipeIdNotFoundException()

        steps = [StepSchema.from_step_model(step) for step in
                 StepRepository.get_steps_by_recipe_id(database, recipe_id)]

        ingredients = [IngredientBaseSchema.from_ingredient_tuple(ingredient[0], ingredient[1], ingredient[2]) for
                       ingredient in
                       RecipeIngredientsRepository.get_recipe_ingredients_by_recipe_id(database, recipe_id)]

        medias = [MediaSchema.from_media_model(media[1]) for
                  media in RecipeMediasRepository.get_all_recipe_medias_data_by_recipe_id(database, recipe_id)]

        return RecipeResponseSchema.from_recipe_models(recipe, steps=steps, ingredients=ingredients, medias=medias)

    @staticmethod
    def delete_a_recipe_by_id(database: Session, recipe_id: int, current_user: UserSchema) -> bool:
        recipe = RecipeRepository.get_recipe_by_id(database, recipe_id)
        if recipe is None:
            raise RecipeIdNotFoundException()
        if recipe.creator_id != current_user.id:
            raise CannotModifyOthersPeopleRecipeException()

        _ = [StepRepository.delete_step_by_id(database, step.id) for step in
             StepRepository.get_steps_by_recipe_id(database, recipe_id)]

        _ = [MediaRepository.delete_media_by_id(database, recipe_media.media_id) for recipe_media in
             RecipeMediasRepository.get_all_recipe_medias_by_recipe_id(database, recipe_id)]

        RecipeIngredientsRepository.delete_recipe_ingredients_by_recipe_id(database, recipe_id)

        RecipeRepository.delete_recipe_by_id(database, recipe_id)
        return True

    @staticmethod
    def update_a_recipe_by_id(database: Session, recipe_id: int, current_user: UserSchema,
                              recipe: RecipeSchema) -> bool:
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

        RecipeIngredientsRepository.delete_recipe_ingredients_by_recipe_id(database, recipe.id)

        for ingredient_bloc in recipe_to_update.ingredients:
            ingredient = IngredientRepository.get_ingredient_by_name(database, ingredient_bloc.ingredient_name)
            if ingredient is None:
                ingredient = IngredientRepository.create_ingredient(database, ingredient_bloc.ingredient_name)

            ingredient_unit = IngredientUnitRepository.get_ingredient_unit_by_name(database,
                                                                                   ingredient_bloc.ingredient_unit)
            if ingredient_unit is None:
                ingredient_unit = IngredientUnitRepository.create_ingredient_unit(database,
                                                                                  ingredient_bloc.ingredient_unit)

            RecipeIngredientsRepository.create_recipe_ingredients(database, recipe_to_update.id, ingredient.id,
                                                                  ingredient_unit.id, ingredient_bloc.quantity)

        StepRepository.create_steps(database, recipe.steps, recipe_id)

        return True

    @staticmethod
    def get_my_wall(database: Session, user: UserSchema) -> List[RecipeResponseSchema]:
        recipes = []
        recipes_list = RecipeRepository.get_followed_recipes(database, user.id)
        for recipe in recipes_list:
            recipes.append(RecipeService.get_a_recipe_by_id(database, recipe.id))
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
            media_category = MediaCategoryRepository.get_media_category_by_name(database,
                                                                                media.content_type.split('/')[0])
            if media_category is None:
                media_category = MediaCategoryRepository.create_media_category(database, MediaCategorySchema(
                    name=media.content_type.split('/')[0], description=media.content_type.split('/')[0]))
            media_schema = MediaBaseSchema(path='temp', media_category_id=media_category.id)
            created_media = MediaRepository.create_media(database, media_schema)
            filename = get_bucket_manager_service().save_file(
                f'{creator_id}/{recipe_id}/{created_media.id}_{media.filename}', media.file)
            created_media.path = filename
            MediaRepository.update_media_by_id(database, created_media.id, filename)
            created_media_ids.append(created_media.id)

            created_medias.append(MediaSchema.from_media_model(created_media))

        RecipeMediasRepository.create_medias(database, created_media_ids, recipe_id)
        return created_medias

    @staticmethod
    def get_all_creator_recipe(database: Session, creator_id: int) -> List[RecipeResponseSchema]:
        recipes = []
        recipes_list = RecipeRepository.get_all_recipe_for_user(database, creator_id)
        for recipe in recipes_list:
            recipes.append(RecipeService.get_a_recipe_by_id(database, recipe.id))
        return recipes

    @staticmethod
    def delete_medias_of_recipe(database: Session, recipe_id: int, creator_id: int, medias: List[MediaSchema]) -> bool:
        recipe_from_db = RecipeRepository.get_recipe_by_id(database, recipe_id)

        if recipe_from_db is None:
            raise RecipeIdNotFoundException()
        if recipe_from_db.creator_id != creator_id:
            raise CannotModifyOthersPeopleRecipeException()

        for media in medias:
            RecipeMediasRepository.delete_recipe_medias_by_recipe_and_media_id(database, recipe_id, media.id)
        return True
