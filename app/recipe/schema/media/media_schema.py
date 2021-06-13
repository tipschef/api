from datetime import datetime
from typing import Optional

from app.recipe.model.media.media_model import MediaModel
from app.recipe.schema.media.media_base_schema import MediaBaseSchema


class MediaSchema(MediaBaseSchema):
    id: Optional[int]
    created_date: Optional[datetime]

    @staticmethod
    def from_media_model(media_model: MediaModel):
        if media_model is None:
            return None
        return MediaSchema(id=media_model.id,
                           created_date=media_model.created_date,
                           path=media_model.path,
                           media_category_id=media_model.media_category_id)

    @staticmethod
    def init():
        return MediaSchema(id=0,
                           path='',
                           media_category_id=0)
