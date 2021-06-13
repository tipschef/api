from pydantic import BaseModel

from app.recipe.model.ingredient.ingredient_model import IngredientModel
from app.recipe.model.ingredient.ingredient_unit_model import IngredientUnitModel
from app.recipe.model.recipe.recipe_ingredients_model import RecipeIngredientsModel


class IngredientBaseSchema(BaseModel):
    ingredient_name: str
    ingredient_unit: str
    quantity: int

    @staticmethod
    def from_ingredient_tuple(recipe_ingredients_model: RecipeIngredientsModel, ingredient_unit: IngredientUnitModel,
                              ingredient: IngredientModel):
        return IngredientBaseSchema(ingredient_name=ingredient.name,
                                    ingredient_unit=ingredient_unit.name,
                                    quantity=recipe_ingredients_model.quantity)
