from dataclasses import dataclass
from typing import List

from sqlalchemy import false
from sqlalchemy.orm import Session


from app.recipe.model.media_category_model import MediaCategoryModel
from app.recipe.schema.media_category_schema import MediaCategorySchema


@dataclass
class MediaCategoryRepository:

    @staticmethod
    def get_all_media_category(database: Session) -> List[MediaCategoryModel]:
        return database.query(MediaCategoryModel).filter(MediaCategoryModel.is_deleted.is_(False)).all()

    @staticmethod
    def get_one_media_category(database: Session, media_category_id: int) -> List[MediaCategoryModel]:
        return database.query(MediaCategoryModel).filter(MediaCategoryModel.is_deleted.is_(False), MediaCategoryModel.id == media_category_id).all()

    @staticmethod
    def create_media_category(database: Session, media_category: MediaCategorySchema) -> MediaCategoryModel:
        db_media_category = MediaCategoryModel(name=media_category.name,
                                               description=media_category.description)
        database.add(db_media_category)
        database.commit()
        database.refresh(db_media_category)
        return db_media_category

    @staticmethod
    def delete_media_category(database: Session, media_category_id: int) -> None:
        database.query(MediaCategoryModel).filter(MediaCategoryModel.is_deleted.is_(False), MediaCategoryModel.id == media_category_id).update({MediaCategoryModel.is_deleted: True})
        database.commit()

    @staticmethod
    def update_media_category(database: Session, media_category_id: int, media_category: MediaCategorySchema) -> None:
        database.query(MediaCategoryModel).filter(
            MediaCategoryModel.is_deleted.is_(False), MediaCategoryModel.id == media_category_id).update(
            {MediaCategoryModel.name: media_category.name, MediaCategoryModel.description: media_category.description})
        database.commit()
