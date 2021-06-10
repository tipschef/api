from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.recipe.recipe_category_schema import RecipeCategoryResponseSchema
from app.recipe.service.recipe_category_service import RecipeCategoryService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/recipe_category')


@router.get('/', response_model=List[RecipeCategoryResponseSchema], tags=['recipe_categories'])
async def get_all_recipe_category(database: Session = Depends(get_database),
                                  _: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeCategoryResponseSchema]:
    try:
        recipe_category_list = RecipeCategoryService.get_all_recipe_categories(database)
        return recipe_category_list
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
