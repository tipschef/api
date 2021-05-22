from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.recipe.model.media_model import MediaModel
from app.recipe.schema.media_schema import MediaBaseSchema


@dataclass
class MediaRepository:

    @staticmethod
    def create_media(database: Session, media: MediaBaseSchema) -> MediaModel:
        db_media = MediaModel(path=media.path, media_category_id=media.media_category_id)
        database.add(db_media)
        database.commit()
        database.refresh(db_media)
        return db_media

    @staticmethod
    def get_media_by_id(database: Session, media_id: int) -> Optional[MediaModel]:
        return database.query(MediaModel).filter(MediaModel.id == media_id, MediaModel.is_deleted.is_(False)).first()

    @staticmethod
    def delete_media_by_id(database: Session, media_id: int) -> None:
        database.query(MediaModel).filter(MediaModel.is_deleted.is_(False), MediaModel.id == media_id).update({MediaModel.is_deleted: True})
        database.commit()

    @staticmethod
    def update_media_by_id(database: Session, media_id: int, path: str) -> None:
        database.query(MediaModel).filter(
            MediaModel.is_deleted.is_(False), MediaModel.id == media_id).update(
            {MediaModel.path: path})
        database.commit()
