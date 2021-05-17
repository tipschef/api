from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.recipe_schema import RecipeSchema
from app.recipe.service.recipe_service import RecipeService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/receipe')


@router.get('/')
async def recipe_route_home():
    return {"message": "Receipe route"}


@router.post('/', response_model=RecipeSchema)
async def create_recipe(recipe: RecipeBaseSchema, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)):
    try:
        recipe_to_create = RecipeSchema.from_recipe_base_schema(recipe, datetime.now(), current_user.id)
        created_recipe_model = RecipeService.create_recipe(database=database, recipe=recipe_to_create)
        return RecipeSchema.from_recipe_model(created_recipe_model)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
