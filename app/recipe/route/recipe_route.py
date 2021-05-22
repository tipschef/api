from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.exception.recipe_service_exceptions import RecipeIdNotFoundException, \
    CannotModifyOthersPeopleRecipeException
from app.recipe.schema.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe_schema import RecipeSchema
from app.recipe.service.recipe_service import RecipeService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe')


@router.get('/', tags=['recipes'])
async def recipe_route_home():
    return {'message': 'Recipe route'}


@router.post('/', response_model=dict, tags=['recipes'])
async def create_recipe(recipe: RecipeBaseSchema, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        recipe_to_create = RecipeSchema.from_recipe_base_schema(recipe, current_user.id)
        created_recipe_id = RecipeService.create_recipe(database, recipe_to_create)
        return {'recipe_id': created_recipe_id, 'status': 'Created'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/me', response_model=List[RecipeSchema], tags=['recipes'])
async def get_my_recipe(database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)):
    try:
        recipe_list = RecipeService.get_all_recipe_for_specific_user(database, current_user.id)
        return recipe_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{recipe_id}', response_model=RecipeResponseSchema, tags=['recipes'])
async def get_a_recipe(recipe_id: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) ->RecipeResponseSchema:
    try:
        recipe = RecipeService.get_a_recipe_by_id(database, recipe_id)
        return recipe
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/{recipe_id}', response_model=dict, tags=['recipes'])
async def delete_a_recipe(recipe_id: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) ->dict:
    try:
        RecipeService.delete_a_recipe_by_id(database, recipe_id)
        return {'status': 'Done'}
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/{recipe_id}', response_model=dict, tags=['recipes'])
async def update_a_recipe(recipe_id: int, recipe: RecipeResponseSchema, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        RecipeService.update_a_recipe_by_id(database, recipe_id, current_user, recipe)
        return {}
    except RecipeIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CannotModifyOthersPeopleRecipeException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


