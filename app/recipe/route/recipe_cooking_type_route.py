from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.recipe.recipe_cooking_type_schema import RecipeCookingTypeResponseSchema
from app.recipe.service.recipe_cooking_type_service import RecipeCookingTypeService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe_cooking_type')


@router.get('/', response_model=List[RecipeCookingTypeResponseSchema], tags=['recipe_cooking_types'])
async def get_all_recipe_cooking_type(database: Session = Depends(get_database),
                                      _: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeCookingTypeResponseSchema]:
    try:
        recipe_cooking_type_list = RecipeCookingTypeService.get_all_recipe_categories(database)
        return recipe_cooking_type_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
