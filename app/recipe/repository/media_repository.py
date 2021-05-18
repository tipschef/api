from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.model.media_model import MediaModel
from app.recipe.schema.media_schema import MediaSchema


@dataclass
class MediaRepository:

    @staticmethod
    def create_media(database: Session, media: MediaSchema) -> MediaModel:
        db_media = MediaModel(path=media.path, media_category_id=media.media_category_id)
        database.add(db_media)
        database.commit()
        database.refresh(db_media)
        return db_media



