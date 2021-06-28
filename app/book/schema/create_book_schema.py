from __future__ import annotations

from typing import List

from pydantic.main import BaseModel

from app.book.schema.recipe_template_schema import RecipeTemplateSchema


class CreateBookSchema(BaseModel):
    name: str
    description: str
    cover_path: str
    description_path: str
    cover_picture_path: str
    recipe_template: List[RecipeTemplateSchema]
