from datetime import datetime

from pydantic import BaseModel

from app.recipe.model.recipe.recipe_category_model import RecipeCategoryModel


class RecipeCategorySchema(BaseModel):
    name: str
    description: str


class RecipeCategoryResponseSchema(RecipeCategorySchema):
    id: int
    created_date: datetime

    @staticmethod
    def from_recipe_category_model(recipe_category: RecipeCategoryModel):
        return RecipeCategoryResponseSchema(name=recipe_category.name,
                                            description=recipe_category.description,
                                            id=recipe_category.id,
                                            created_date=recipe_category.created_date)
