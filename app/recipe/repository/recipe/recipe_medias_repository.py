from dataclasses import dataclass
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.recipe.model.media.media_model import MediaModel
from app.recipe.model.recipe.recipe_medias_model import RecipeMediasModel


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

    @staticmethod
    def delete_recipe_medias_by_recipe_id(database: Session, recipe_id: int) -> None:
        database.query(RecipeMediasModel).filter(RecipeMediasModel.recipe_id == recipe_id).delete()
        database.commit()

    @staticmethod
    def get_all_recipe_medias_by_recipe_id(database: Session, recipe_id: int) -> List[RecipeMediasModel]:
        return database.query(RecipeMediasModel).filter(RecipeMediasModel.recipe_id == recipe_id).all()

    @staticmethod
    def get_all_recipe_medias_data_by_recipe_id(database: Session, recipe_id: int) -> List[Tuple[RecipeMediasModel, MediaModel]]:
        return database.query(RecipeMediasModel, MediaModel)\
                       .filter(RecipeMediasModel.recipe_id == recipe_id)\
                       .filter(RecipeMediasModel.media_id == MediaModel.id)\
                       .all()
