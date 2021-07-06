from typing import List

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.book.exception.book_service_exception import BookIdNotFoundException, UniqueIdDoesNotMatch, \
    CannotModifyOthersPeopleBookException, AlreadyHaveBookException
from app.book.schema.book_purchase_schema import BookPurchaseSchema
from app.book.schema.book_schema import BookSchema
from app.book.schema.create_book_schema import CreateBookSchema
from app.book.schema.template_list_schema import TemplateListSchema
from app.book.service.book_service import BookService
from app.database.service.database_instance import get_database
from app.payment.exception.payment_service_exceptions import NoPaymentMethodException
from app.user.schema.user.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/book')


@router.post('/broker', response_model=BookSchema, tags=['books'])
async def create_book(create_book_schema: CreateBookSchema, database: Session = Depends(get_database),
                      current_user: UserSchema = Depends(UserService.get_current_active_user)) -> BookSchema:
    try:
        book = BookService.create_book(database, create_book_schema, current_user)
        return book
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/template', response_model=TemplateListSchema, tags=['books'])
async def get_template() -> TemplateListSchema:
    try:
        return BookService.get_templates()
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/creator', response_model=List[BookSchema], tags=['books'])
async def get_my_books(database: Session = Depends(get_database),
                       current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[BookSchema]:
    try:
        return BookService.get_my_books(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/cover', response_model=dict, tags=['books'])
async def post_cover(cover: UploadFile = File(...),
                     current_user: UserSchema = Depends(
                         UserService.get_current_active_user)) -> dict:
    try:
        filename = BookService.post_cover(current_user.id, cover)
        return {'url': filename}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/recipe/{recipe_id}', response_model=List[BookSchema], tags=['books'])
async def get_book_by_recipe(recipe_id: int, database: Session = Depends(get_database),
                             _: UserSchema = Depends(UserService.get_current_active_user)) -> List[BookSchema]:
    try:
        return BookService.get_book_by_recipe(database, recipe_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/user/{username}', response_model=List[BookSchema], tags=['books'])
async def get_book_by_creator(username: str, database: Session = Depends(get_database),
                              _: UserSchema = Depends(UserService.get_current_active_user)) -> List[BookSchema]:
    try:
        return BookService.get_book_by_creator(database, username)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/check/{book_id}', response_model=dict, tags=['books', 'payment'])
async def check_already_bought(book_id: int, database: Session = Depends(get_database),
                               current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        return {'is_bought': BookService.check_already_bought(database, current_user, book_id)}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/buy', response_model=List[BookPurchaseSchema], tags=['books', 'payment'])
async def get_my_book_history(database: Session = Depends(get_database),
                              current_user: UserSchema = Depends(UserService.get_current_active_user))\
        -> List[BookPurchaseSchema]:
    try:
        return BookService.get_book_purchase_history_by_user(database, current_user)
    except AlreadyHaveBookException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/buy/{book_id}', response_model=dict, tags=['books', 'payment'])
async def buy_book_by_id(book_id: int, database: Session = Depends(get_database),
                         current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        BookService.buy_book_by_id(database, book_id, current_user)
        return {'status': 'Done'}
    except BookIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except NoPaymentMethodException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{book_id}', response_model=BookSchema, tags=['books'])
async def get_book_by_id(book_id: int, database: Session = Depends(get_database),
                         _: UserSchema = Depends(UserService.get_current_active_user)) -> BookSchema:
    try:
        return BookService.get_book_by_id(database, book_id)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/pdf/{book_id}/{u_id}', response_model=dict, tags=['books'])
async def add_pdf_to_book(book_id: int, u_id: str, file: UploadFile = File(...),
                          database: Session = Depends(get_database)) \
        -> dict:
    try:
        BookService.add_pdf_to_book(database, book_id, u_id, file)
        return {'message': 'done'}
    except BookIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except UniqueIdDoesNotMatch as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.delete('/{book_id}', response_model=dict, tags=['books'])
async def delete_a_recipe(book_id: int, database: Session = Depends(get_database),
                          current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        BookService.delete_a_book_by_id(database, book_id, current_user)
        return {'status': 'Done'}
    except BookIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except CannotModifyOthersPeopleBookException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
