from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.database.service.database_init import init_data
from app.database.service.database_instance import get_database
from app.recipe.exception.recipe_service_exceptions import RecipeIdNotFoundException, \
    CannotModifyOthersPeopleRecipeException, NotRecipeOwnerException, UserNotAuthorized, WrongUserToDeleteComment
from app.recipe.schema.comment.comment_input_schema import CommentInputSchema
from app.recipe.schema.comment.comment_output_base_schema import CommentOutputBaseSchema
from app.recipe.schema.like.like_schema import LikeSchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe.recipe_response_extended_schema import RecipeResponseExtendedSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe.recipe_schema import RecipeSchema
from app.recipe.service.comment_service import CommentService
from app.recipe.service.like_service import LikeService
from app.recipe.service.recipe_service import RecipeService
from app.user.schema.user.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe')


@router.get('/', tags=['recipes'])
async def recipe_route_home():
    return {'message': 'Recipe route'}


@router.post('/', response_model=dict, tags=['recipes'])
async def create_recipe(recipe: RecipeBaseSchema, database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        created_recipe_id = RecipeService.create_recipe(database, recipe, current_user.id)
        return {'recipe_id': created_recipe_id, 'status': 'Created'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/media/{recipe_id}', response_model=List[MediaSchema], tags=['recipes'])
async def add_medias_to_recipe(recipe_id: int, files: List[UploadFile] = File(...),
                               database: Session = Depends(get_database),
                               current_user: UserSchema = Depends(UserService.get_current_active_user))\
        -> List[MediaSchema]:
    try:
        medias = RecipeService.add_media_to_recipe(database, current_user.id, recipe_id, files)
        return medias
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except NotRecipeOwnerException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/thumbnail_media/{recipe_id}', response_model=MediaSchema, tags=['recipes'])
async def add_thumbnail_media_to_recipe(recipe_id: int, thumbnail: UploadFile = File(...),
                                        database: Session = Depends(get_database),
                                        current_user: UserSchema = Depends(
                                            UserService.get_current_active_user)) -> MediaSchema:
    try:
        medias = RecipeService.add_thumbnail_to_recipe(database, recipe_id, current_user.id, thumbnail)
        return medias
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except NotRecipeOwnerException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/video_media/{recipe_id}', response_model=MediaSchema, tags=['recipes'])
async def add_video_media_to_recipe(recipe_id: int, video: UploadFile = File(...),
                                    database: Session = Depends(get_database),
                                    current_user: UserSchema = Depends(
                                        UserService.get_current_active_user)) -> MediaSchema:
    try:
        medias = RecipeService.add_video_to_recipe(database, recipe_id, current_user.id, video)
        return medias
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except NotRecipeOwnerException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/init', response_model=dict, tags=['recipes', 'admin'])
async def init_database(database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        init_data(database, current_user)
        return {'message': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/liked_recipe', response_model=List[RecipeResponseExtendedSchema], tags=['recipes', 'wall'])
async def get_liked_recipe(per_page: int = 20, page: int = 1, database: Session = Depends(get_database),
                           current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeResponseExtendedSchema]:
    try:
        return RecipeService.get_all_liked_recipes(database, current_user, per_page, page)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/wall', response_model=List[RecipeResponseExtendedSchema], tags=['recipes', 'wall'])
async def get_my_wall(per_page: int = 20, page: int = 1, database: Session = Depends(get_database),
                      current_user: UserSchema = Depends(UserService.get_current_active_user))\
        -> List[RecipeResponseExtendedSchema]:
    try:
        return RecipeService.get_my_wall(database, current_user, per_page, page)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/creator', response_model=List[RecipeResponseSchema], tags=['recipes'])
async def get_all_creator_recipe(database: Session = Depends(get_database),
                                 current_user: UserSchema = Depends(UserService.get_current_active_user))\
        -> List[RecipeResponseSchema]:
    try:
        return RecipeService.get_all_creator_recipe(database, current_user.id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}', response_model=RecipeResponseSchema, tags=['recipes'])
async def get_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                       asking_user: UserSchema = Depends(UserService.get_current_active_user)) -> RecipeResponseSchema:
    try:
        recipe = RecipeService.get_a_recipe_by_id_and_asking_user(database, recipe_id, asking_user)
        return recipe
    except UserNotAuthorized as exception:
        raise HTTPException(status_code=403, detail=exception.as_dict())
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/{recipe_id}', response_model=dict, tags=['recipes'])
async def delete_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                          current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        RecipeService.delete_a_recipe_by_id(database, recipe_id, current_user)
        return {'status': 'Done'}
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CannotModifyOthersPeopleRecipeException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.put('/media/{recipe_id}', response_model=dict, tags=['recipes'])
async def delete_media_from_recipe(recipe_id: int, medias: List[MediaSchema], database: Session = Depends(get_database),
                                   current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        RecipeService.delete_medias_of_recipe(database, recipe_id, current_user.id, medias)
        return {'status': 'Done'}
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CannotModifyOthersPeopleRecipeException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/{recipe_id}', response_model=dict, tags=['recipes'])
async def update_a_recipe(recipe_id: int, recipe: RecipeSchema, database: Session = Depends(get_database),
                          current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        RecipeService.update_a_recipe_by_id(database, recipe_id, current_user, recipe)
        return {'status': 'Done'}
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CannotModifyOthersPeopleRecipeException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/{recipe_id}/like', response_model=dict, tags=['recipes', 'like'])
async def like_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if LikeService.like_someone_by_id(database, current_user, recipe_id):
            return {'Status': 'Done'}
        return {'Status': 'You already Liked this recipe'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/{recipe_id}/dislike', response_model=dict, tags=['recipes', 'like'])
async def dislike_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                           current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if LikeService.dislike_someone_by_id(database, current_user, recipe_id):
            return {'Status': 'Done'}
        return {'Status': 'You have not liked this recipe'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}/like', response_model=LikeSchema, tags=['recipes', 'like'])
async def get_like_from_recipe(recipe_id: int, database: Session = Depends(get_database),
                               current_user: UserSchema = Depends(UserService.get_current_active_user)) -> LikeSchema:
    try:
        return LikeService.get_like_by_recipe_id(database, recipe_id, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/{recipe_id}/comment', response_model=dict, tags=['recipes', 'comments'])
async def add_comment_to_recipe(recipe_id: int, comment: CommentInputSchema, database: Session = Depends(get_database),
                                current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        CommentService.create_comment_on_a_recipe(database, current_user, comment, recipe_id)
        return {'Status': 'Done'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/{recipe_id}/comment/{comment_id}', response_model=dict, tags=['recipes', 'comments'])
async def remove_comment_from_recipe(recipe_id: int, comment_id: int, database: Session = Depends(get_database),
                                     current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        CommentService.delete_comment_by_id(database, current_user, comment_id, recipe_id)
        return {'Status': 'Done'}
    except WrongUserToDeleteComment as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}/comment', response_model=List[CommentOutputBaseSchema], tags=['recipes', 'comments'])
async def get_all_comment_from_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                                        _: UserSchema = Depends(UserService.get_current_active_user))\
        -> List[CommentOutputBaseSchema]:
    try:
        return CommentService.get_comments_by_recipe_id(database, recipe_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
