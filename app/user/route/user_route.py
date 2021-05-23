from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.user.exception.user_route_exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, \
    UserNotFoundException
from app.user.schema.user_detailed_schema import UserDetailedSchema
from app.user.schema.user_create_schema import UserCreateSchema
from app.user.schema.user_schema import UserSchema
from app.user.service.follow_service import FollowService
from app.user.service.user_service import UserService

router = APIRouter(prefix='/users')


@router.get('/', tags=['users'])
async def user_route():
    return {'message': 'User route'}


@router.post("/", response_model=UserSchema, tags=['users'])
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


@router.get('/{user_id}', response_model=UserDetailedSchema, tags=['users'])
async def get_user_by_id(user_id: int, database: Session = Depends(get_database)) -> UserDetailedSchema:
    try:
        return UserService.get_user_by_id(database, user_id)
    except UserNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{user_id}/follow', response_model=dict, tags=['users', 'follow'])
async def follow_user_by_id(user_id: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if FollowService.follow_someone_by_id(database, current_user, user_id):
            return {'Status': 'Done'}
        return {'Status': 'Already following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{user_id}/unfollow', response_model=dict, tags=['users', 'follow'])
async def unfollow_user_by_id(user_id: int, database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:

        if FollowService.unfollow_someone_by_id(database, current_user, user_id):
            return {'Status': 'Done'}
        return {'Status': 'You were not following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
