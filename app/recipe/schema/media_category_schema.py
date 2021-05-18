from datetime import datetime

from pydantic import BaseModel

from app.recipe.model.media_category_model import MediaCategoryModel


class MediaCategorySchema(BaseModel):
    name: str
    description: str


class MediaCategoryResponseSchema(MediaCategorySchema):
    id: int
    created_date: datetime

    @staticmethod
    def from_media_category_model(media_category: MediaCategoryModel):
        return MediaCategoryResponseSchema(name=media_category.name,
                                           description=media_category.description,
                                           id=media_category.id,
                                           created_date=media_category.created_date)
