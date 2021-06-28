from __future__ import annotations

from pydantic.main import BaseModel


class RecipeTemplateSchema(BaseModel):
    recipe_id: int
    template_path: str