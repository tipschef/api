from datetime import datetime

from pydantic import BaseModel

from app.recipe.model.recipe.recipe_cooking_type_model import RecipeCookingTypeModel


class RecipeCookingTypeSchema(BaseModel):
    name: str
    description: str


class RecipeCookingTypeResponseSchema(RecipeCookingTypeSchema):
    id: int
    created_date: datetime

    @staticmethod
    def from_recipe_cooking_type_model(recipe_cooking_type: RecipeCookingTypeModel):
        return RecipeCookingTypeResponseSchema(name=recipe_cooking_type.name,
                                               description=recipe_cooking_type.description,
                                               id=recipe_cooking_type.id,
                                               created_date=recipe_cooking_type.created_date)
