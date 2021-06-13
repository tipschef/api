from dataclasses import dataclass
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.recipe.model.ingredient.ingredient_model import IngredientModel
from app.recipe.model.ingredient.ingredient_unit_model import IngredientUnitModel
from app.recipe.model.recipe.recipe_ingredients_model import RecipeIngredientsModel


@dataclass
class RecipeIngredientsRepository:
    @staticmethod
    def create_recipe_ingredients(database: Session, recipe_id: int, ingredient_id: int, ingredient_unit_id: int, quantity: int) -> RecipeIngredientsModel:
        db_recipe_ingredients = RecipeIngredientsModel(recipe_id=recipe_id, ingredient_id=ingredient_id, ingredient_unit_id=ingredient_unit_id, quantity=quantity)
        database.add(db_recipe_ingredients)
        database.commit()
        database.refresh(db_recipe_ingredients)
        return db_recipe_ingredients

    @staticmethod
    def delete_recipe_ingredients_by_recipe_id(database: Session, recipe_id: int) -> None:
        database.query(RecipeIngredientsModel).filter(RecipeIngredientsModel.recipe_id == recipe_id).delete()
        database.commit()

    @staticmethod
    def get_recipe_ingredients_by_recipe_id(database: Session, recipe_id: int) -> List[Tuple[RecipeIngredientsModel, IngredientUnitModel, IngredientModel]]:
        return database.query(RecipeIngredientsModel, IngredientUnitModel, IngredientModel)\
                       .filter(RecipeIngredientsModel.recipe_id == recipe_id)\
                       .filter(RecipeIngredientsModel.ingredient_unit_id == IngredientUnitModel.id)\
                       .filter(RecipeIngredientsModel.ingredient_id == IngredientModel.id)\
                       .all()
