from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.recipe.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe.recipe_schema import RecipeSchema
from app.user.model.follow_model import FollowModel


@dataclass
class RecipeRepository:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeBaseSchema, creator_id: int) -> RecipeModel:
        db_recipe = RecipeModel(min_tier=recipe.min_tier,
                                name=recipe.name,
                                description=recipe.description,
                                recipe_cooking_type_id=recipe.recipe_cooking_type_id,
                                recipe_category_id=recipe.recipe_category_id,
                                portion_number=recipe.portion_number,
                                portion_unit=recipe.portion_unit,
                                preparation_hours=recipe.preparation_hours,
                                preparation_minutes=recipe.preparation_minutes,
                                cooking_hours=recipe.cooking_hours,
                                cooking_minutes=recipe.cooking_minutes,
                                resting_hours=recipe.resting_hours,
                                resting_minutes=recipe.resting_minutes,
                                difficulty=recipe.difficulty,
                                cost=recipe.cost,
                                creator_id=creator_id)
        database.add(db_recipe)
        database.commit()
        database.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def get_all_recipe_for_user(database: Session, user_id: int) -> List[RecipeModel]:
        return database.query(RecipeModel).filter(RecipeModel.creator_id == user_id, RecipeModel.is_deleted.is_(False)).all()

    @staticmethod
    def get_recipe_by_id(database: Session, recipe_id: int) -> Optional[RecipeModel]:
        return database.query(RecipeModel).filter(RecipeModel.id == recipe_id, RecipeModel.is_deleted.is_(False)).first()

    @staticmethod
    def delete_recipe_by_id(database: Session, recipe_id: int) -> None:
        database.query(RecipeModel).filter(RecipeModel.is_deleted.is_(False), RecipeModel.id == recipe_id).update({RecipeModel.is_deleted: True})
        database.commit()

    @staticmethod
    def update_recipe_by_id(database: Session, recipe_id: int, recipe: RecipeSchema, ) -> None:
        database.query(RecipeModel).filter(RecipeModel.is_deleted.is_(False), RecipeModel.id == recipe_id)\
                                   .update({RecipeModel.min_tier: recipe.min_tier,
                                            RecipeModel.portion_number: recipe.portion_number,
                                            RecipeModel.portion_unit: recipe.portion_unit,
                                            RecipeModel.preparation_hours: recipe.preparation_hours,
                                            RecipeModel.preparation_minutes: recipe.preparation_minutes,
                                            RecipeModel.cooking_hours: recipe.cooking_hours,
                                            RecipeModel.cooking_minutes: recipe.cooking_minutes,
                                            RecipeModel.resting_hours: recipe.resting_hours,
                                            RecipeModel.resting_minutes: recipe.resting_minutes,
                                            RecipeModel.difficulty: recipe.difficulty,
                                            RecipeModel.cost: recipe.cost,
                                            RecipeModel.name: recipe.name,
                                            RecipeModel.description: recipe.description,
                                            RecipeModel.recipe_category_id: recipe.recipe_category_id,
                                            RecipeModel.recipe_cooking_type_id: recipe.recipe_cooking_type_id,
                                            RecipeModel.last_updated: datetime.utcnow()})
        database.commit()

    @staticmethod
    def get_followed_recipes(database: Session, user_id: int) -> List[RecipeModel]:
        sub_query = database.query(FollowModel.followed_id).filter(FollowModel.follower_id == user_id)
        return database.query(RecipeModel).filter(RecipeModel.creator_id.in_(sub_query), RecipeModel.is_deleted.is_(False)).all()
