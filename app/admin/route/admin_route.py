from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.admin.schema.user_admin_schema import UserAdminSchema
from app.admin.service.admin_service import AdminService
from app.database.service.database_instance import get_database
from app.payment.exception.payment_service_exceptions import NoAccountIdException
from app.payment.service.payment_service import get_payment_service
from app.user.schema.user.user_schema import UserSchema
from app.user.service.dashboard_service import DashboardService
from app.user.service.user_service import UserService

router = APIRouter(prefix='/admin')


@router.get('/', tags=['admin'])
async def admin_route():
    return {'message': 'admin route'}


@router.patch('/partner/add/{user_id}', response_model=dict, tags=['admin'])
async def set_user_as_partner(user_id: int, database: Session = Depends(get_database),
                              current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.set_user_to_partner(database, user_id, current_user)
        return {'status': 'Done'}
    except NoAccountIdException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/partner/remove/{user_id}', response_model=dict, tags=['admin'])
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


@router.get('/users', response_model=List[UserAdminSchema], tags=['admin'])
async def get_users(database: Session = Depends(get_database),
                    current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[UserAdminSchema]:
    try:
        return AdminService.get_users(database, current_user)
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/highlight/add/{user_id}', response_model=dict, tags=['admin'])
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


@router.patch('/admin/add/{user_id}', response_model=dict, tags=['admin'])
async def add_admin(user_id: int, database: Session = Depends(get_database),
                    current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        AdminService.add_admin_user_by_id(database, user_id, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/highlight/remove/{user_id}', response_model=dict, tags=['admin'])
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


@router.post('/payment', response_model=dict, tags=['admin', 'payment', 'payslip'])
async def pay_user_by_id(database: Session = Depends(get_database),
                         current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        get_payment_service().pay_every_partner(database, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except NoAccountIdException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/dashboard/generate', response_model=dict, tags=['admin', 'dashboard'])
async def generate_dashboard_data(database: Session = Depends(get_database),
                                  current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        DashboardService.create_dashboard_data(database, current_user)
        return {'status': 'Done'}
    except UserNotAdminException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
