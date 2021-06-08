from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.schema.recipe.recipe_response_extended_schema import RecipeResponseExtendedSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.service.recipe_service import RecipeService
from app.user.exception.user_route_exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, \
    UserNotFoundException
from app.user.schema.user_detailed_schema import UserDetailedSchema
from app.user.schema.user_create_schema import UserCreateSchema
from app.user.schema.user_schema import UserSchema
from app.user.service.follow_service import FollowService
from app.user.service.subscription_service import SubscriptionService
from app.user.service.user_service import UserService

router = APIRouter(prefix='/users')


@router.get('/', tags=['users'])
async def user_route():
    return {'message': 'User route'}


@router.post('/', response_model=UserSchema, tags=['users'])
async def create_user_route(user: UserCreateSchema, database: Session = Depends(get_database)):
    try:
        created_user_model = UserService.create_user(database=database, user=user)
        return UserSchema.from_user_model(created_user_model)
    except UserAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except UsernameAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}', response_model=UserDetailedSchema, tags=['users'])
async def get_user_by_username(username: str, database: Session = Depends(get_database)) -> UserDetailedSchema:
    try:
        return UserService.get_user_by_username(database, username)
    except UserNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/follow', response_model=dict, tags=['users', 'follow'])
async def follow_user_by_username(username: str, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if FollowService.follow_someone_by_username(database, current_user, username):
            return {'Status': 'Done'}
        return {'Status': 'Already following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/unfollow', response_model=dict, tags=['users', 'follow'])
async def unfollow_user_by_username(username: str, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:

        if FollowService.unfollow_someone_by_username(database, current_user, username):
            return {'Status': 'Done'}
        return {'Status': 'You were not following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/recipes', response_model=List[RecipeResponseExtendedSchema], tags=['users', 'recipes'])
async def get_recipes_from_username(username: str, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[RecipeResponseExtendedSchema]:
    try:
        return RecipeService.get_all_recipe_for_specific_user(database, current_user, username)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/subscribe', response_model=dict, tags=['users', 'subscribe'])
async def subscribe_by_username(username: str, tier: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if SubscriptionService.subscribe_to_someone_by_username(database, current_user, username, tier):
            return {'Status': 'Done'}
        return {'Status': 'Already subscribed'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/unsubscribe', response_model=dict, tags=['users', 'subscribe'])
async def unsubscribe_by_username(username: str, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if SubscriptionService.unsubscribe_to_someone_by_username(database, current_user, username):
            return {'Status': 'Done'}
        return {'Status': 'You were not subscribed'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/subscribe/{receiver}', response_model=dict, tags=['users', 'subscribe'])
async def unsubscribe_by_username(username: str, receiver: str, tier: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if SubscriptionService.gift_a_subscription_to_someone_by_username(database, current_user, username, receiver, tier):
            return {'Status': 'Done'}
        return {'Status': 'You were not subscribed'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
