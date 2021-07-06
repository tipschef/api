from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from stripe import Account

from app.database.service.database_instance import get_database
from app.payment.exception.payment_service_exceptions import UserNotCookException, NoAccountIdException, \
    NoPaymentMethodException
from app.payment.schema.bank_account_schema import BankAccountSchema
from app.payment.schema.card_schema import CardSchema
from app.payment.schema.payment_schema import PaymentSchema
from app.payment.schema.payslip_schema import PayslipSchema
from app.payment.service.payment_service import get_payment_service
from app.user.schema.user.user_auth_schema import UserAuthSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/payment')


@router.post('/account/create', response_model=Account, tags=['payment', 'partner'])
async def create_account_payment(payment: PaymentSchema, database: Session = Depends(get_database),
                                 current_user: UserAuthSchema = Depends(
                                     UserService.get_current_active_user)) -> Account:
    try:
        return get_payment_service().create_account(database, payment, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/account/', response_model=PaymentSchema, tags=['payment', 'partner'])
async def get_my_account_information(database: Session = Depends(get_database),
                                     current_user: UserAuthSchema = Depends(
                                         UserService.get_current_active_user)) -> PaymentSchema:
    try:
        account = get_payment_service().get_account_by_id(database, current_user)
        return PaymentSchema.from_account(account)
    except NoAccountIdException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/bank_account/create', response_model=Account, tags=['payment', 'partner'])
async def create_bank_account(bank_account: BankAccountSchema, database: Session = Depends(get_database),
                              current_user: UserAuthSchema = Depends(UserService.get_current_active_user)) -> Account:
    try:
        return get_payment_service().create_bank_account(database, current_user, bank_account)
    except NoAccountIdException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/payment_method/create', response_model=Account, tags=['payment', 'partner'])
async def create_payment_method(card: CardSchema, database: Session = Depends(get_database),
                                current_user: UserAuthSchema = Depends(UserService.get_current_active_user)) -> Account:
    try:
        return get_payment_service().create_payment_method(database, current_user, card)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/payment_method', response_model=dict, tags=['payment', 'partner'])
async def get_payment_method(database: Session = Depends(get_database),
                             current_user: UserAuthSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        response = get_payment_service().get_payment_method_information(database, current_user)
        return {'card_number': response}
    except NoPaymentMethodException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/payment_method', response_model=dict, tags=['payment', 'partner'])
async def detach_payment_method(database: Session = Depends(get_database),
                                current_user: UserAuthSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        get_payment_service().delete_payment_method(database, current_user)
        return {'status': 'done'}
    except NoPaymentMethodException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/account/id', response_model=dict, tags=['payment', 'partner'])
async def upload_id_picture(file: UploadFile = File(...),
                            _: UserAuthSchema = Depends(
                                UserService.get_current_active_user)) -> dict:
    try:
        return get_payment_service().upload_id(file)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/account/', response_model=dict, tags=['payment', 'partner'])
async def delete_my_account(database: Session = Depends(get_database),
                            current_user: UserAuthSchema = Depends(
                                UserService.get_current_active_user)) -> dict:
    try:
        if current_user.is_partner is True:
            return get_payment_service().delete_account(database, current_user)
        raise UserNotCookException()
    except UserNotCookException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except NoAccountIdException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/payslip/', response_model=List[PayslipSchema], tags=['payment', 'payslip', 'partner'])
async def get_my_payslips(database: Session = Depends(get_database),
                          current_user: UserAuthSchema = Depends(
                              UserService.get_current_active_user)) -> List[PayslipSchema]:
    try:
        if current_user.is_partner is True:
            return get_payment_service().get_my_payslips(database, current_user)
        raise UserNotCookException()
    except UserNotCookException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
