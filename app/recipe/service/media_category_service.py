from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.repository.media_category_repository import MediaCategoryRepository
from app.recipe.schema.media_category_schema import MediaCategorySchema, MediaCategoryResponseSchema


@dataclass
class MediaCategoryService:
    @staticmethod
    def get_all_media_category(database: Session) -> List[MediaCategoryResponseSchema]:
        media_category_list = MediaCategoryRepository.get_all_media_category(database)
        return [MediaCategoryResponseSchema.from_media_category_model(media_category) for media_category in media_category_list]

    @staticmethod
    def create_media_category(database: Session, media_category: MediaCategorySchema) -> MediaCategoryResponseSchema:
        media_category = MediaCategoryRepository.create_media_category(database, media_category)
        return MediaCategoryResponseSchema.from_media_category_model(media_category)

    @staticmethod
    def delete_media_category(database: Session, media_category_id: int) -> bool:
        MediaCategoryRepository.delete_media_category(database, media_category_id)
        return True

    @staticmethod
    def update_media_category(database: Session, media_category_id: int, media_category: MediaCategorySchema) -> None:
        media_category = MediaCategoryRepository.update_media_category(database, media_category_id, media_category)
        # return MediaCategoryResponseSchema.from_media_category_model(media_category)
        return None
