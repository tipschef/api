from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.exception.recipe_service_exceptions import RecipeIdNotFoundException, \
    CannotModifyOthersPeopleRecipeException
from app.recipe.schema.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe_schema import RecipeSchema
from app.recipe.service.like_service import LikeService
from app.recipe.service.recipe_service import RecipeService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe')


@router.get('/', tags=['recipes'])
async def recipe_route_home():
    return {'message': 'Recipe route'}


@router.post('/', response_model=dict, tags=['recipes'])
async def create_recipe(recipe: RecipeBaseSchema, database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        recipe_to_create = RecipeSchema.from_recipe_base_schema(recipe, current_user.id)
        created_recipe_id = RecipeService.create_recipe(database, recipe_to_create)
        return {'recipe_id': created_recipe_id, 'status': 'Created'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/{recipe_id}/media', response_model=dict, tags=['recipes'])
async def create_recipe(recipe_id: int, files: List[UploadFile] = File(...), database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    print(recipe_id)
    print(files)
    print(files[0].file, files[0].filename, files[0].content_type)


@router.get('/me', response_model=List[RecipeResponseSchema], tags=['recipes'])
async def get_my_recipe(database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeResponseSchema]:
    try:
        recipe_list = RecipeService.get_all_recipe_for_specific_user(database, current_user.id)
        return recipe_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/wall', response_model=List[RecipeResponseSchema], tags=['recipes', 'wall'])
async def get_my_wall(database: Session = Depends(get_database),
                      current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeResponseSchema]:
    try:
        return RecipeService.get_my_wall(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}', response_model=RecipeResponseSchema, tags=['recipes'])
async def get_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                       _: UserSchema = Depends(UserService.get_current_active_user)) -> RecipeResponseSchema:
    try:
        recipe = RecipeService.get_a_recipe_by_id(database, recipe_id)
        return recipe
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


@router.patch('/{recipe_id}', response_model=dict, tags=['recipes'])
async def update_a_recipe(recipe_id: int, recipe: RecipeResponseSchema, database: Session = Depends(get_database),
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


@router.get('/{recipe_id}/like', response_model=dict, tags=['recipes', 'like'])
async def like_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                        current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if LikeService.like_someone_by_id(database, current_user, recipe_id):
            return {'Status': 'Done'}
        return {'Status': 'You already Liked this recipe'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}/dislike', response_model=dict, tags=['recipes', 'like'])
async def dislike_a_recipe(recipe_id: int, database: Session = Depends(get_database),
                           current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if LikeService.dislike_someone_by_id(database, current_user, recipe_id):
            return {'Status': 'Done'}
        return {'Status': 'You have not liked this recipe'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
