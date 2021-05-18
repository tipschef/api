from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe_schema import RecipeSchema
from app.recipe.service.recipe_service import RecipeService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe')


@router.get('/')
async def recipe_route_home():
    return {"message": "Recipe route"}


@router.post('/', response_model=RecipeSchema)
async def create_recipe(recipe: RecipeBaseSchema, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> RecipeSchema:
    try:
        recipe_to_create = RecipeSchema.from_recipe_base_schema(recipe, current_user.id)
        created_recipe = RecipeService.create_recipe(database=database, recipe=recipe_to_create)
        return created_recipe
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/me', response_model=List[RecipeSchema])
async def get_my_recipe(database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)):
    try:
        recipe_list = RecipeService.get_all_recipe_for_specific_user(database=database, user_id=current_user.id)
        return recipe_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
