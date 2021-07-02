from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.admin.service.admin_service import AdminService
from app.database.service.database_instance import get_database
from app.user.schema.user.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/admin')


@router.get('/', tags=['admin'])
async def admin_route():
    return {'message': 'admin route'}


@router.post('/partner/{user_id}', response_model=dict, tags=['admin'])
async def set_user_as_partner(user_id: int, database: Session = Depends(get_database),
                              current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.set_user_to_partner(database, user_id, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/partner/{user_id}', response_model=dict, tags=['admin'])
async def remove_user_partner(user_id: int, database: Session = Depends(get_database),
                              current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.remove_user_partner(database, user_id, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/highlight/{user_id}', response_model=dict, tags=['admin'])
async def highlight_people(user_id: int, database: Session = Depends(get_database),
                           current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.highlight_user_by_id(database, user_id, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/highlight/{user_id}', response_model=dict, tags=['admin'])
async def remove_highlighted_people(user_id: int, database: Session = Depends(get_database),
                                    current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.remove_highlight_user_by_id(database, user_id, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
