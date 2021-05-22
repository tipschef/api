from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.media_category_schema import MediaCategorySchema, MediaCategoryResponseSchema
from app.recipe.service.media_category_service import MediaCategoryService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/media_category')


@router.get('/', response_model=List[MediaCategoryResponseSchema], tags=['media_categories'])
async def get_all_media_category(database: Session = Depends(get_database),
                                 current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[
    MediaCategoryResponseSchema]:
    try:
        media_category_list = MediaCategoryService.get_all_media_category(database)
        return media_category_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/', response_model=MediaCategoryResponseSchema, tags=['media_categories'])
async def create_media_category(media_category: MediaCategorySchema, database: Session = Depends(get_database),
                                current_user: UserSchema = Depends(
                                    UserService.get_current_active_user)) -> MediaCategoryResponseSchema:
    try:
        media_category = MediaCategoryService.create_media_category(database, media_category)
        return media_category
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/{media_category_id}', response_model=dict, tags=['media_categories'])
async def delete_media_category(media_category_id: int, database: Session = Depends(get_database),
                                current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        MediaCategoryService.delete_media_category(database, media_category_id)
        return {'status': 'Done'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/{media_category_id}', response_model=dict, tags=['media_categories'])
async def update_media_category(media_category_id: int, media_category: MediaCategorySchema,
                                database: Session = Depends(get_database),
                                current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        MediaCategoryService.update_media_category(database, media_category_id, media_category)
        return {'status': 'Done'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
