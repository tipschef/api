from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.model.recipe_ingredients_model import RecipeIngredientsModel


@dataclass
class RecipeIngredientsRepository:
    @staticmethod
    def create_recipe_ingredients(database: Session, recipe_id: int, ingredient_id: int, ingredient_unit_id: int, quantity: int) -> RecipeIngredientsModel:
        db_recipe_ingredients = RecipeIngredientsModel(recipe_id=recipe_id, ingredient_id=ingredient_id, ingredient_unit_id=ingredient_unit_id, quantity=quantity)
        database.add(db_recipe_ingredients)
        database.commit()
        database.refresh(db_recipe_ingredients)
        return db_recipe_ingredients
