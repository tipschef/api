from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.recipe_medias_model import RecipeMediasModel


@dataclass
class RecipeMediasRepository:

    @staticmethod
    def create_media(database: Session, recipe_id: int, media_id: int) -> RecipeMediasModel:
        db_recipe_media = RecipeMediasModel(recipe_id=recipe_id, media_id=media_id)
        database.add(db_recipe_media)
        database.commit()
        database.refresh(db_recipe_media)
        return db_recipe_media

    @staticmethod
    def create_medias(database: Session, media_ids: List[int], recipe_id: int) -> None:
        db_step_list = [RecipeMediasModel(recipe_id=recipe_id, media_id=media_id) for media_id in media_ids]
        database.bulk_save_objects(db_step_list)
        database.commit()
