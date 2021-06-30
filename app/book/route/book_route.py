from typing import List

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.book.exception.book_service_exception import BookIdNotFoundException, UniqueIdDoesNotMatch, \
    CannotModifyOthersPeopleBookException
from app.book.schema.book_schema import BookSchema
from app.book.schema.create_book_schema import CreateBookSchema
from app.book.schema.preview_schema import PreviewSchema
from app.book.schema.template_list_schema import TemplateListSchema
from app.book.service.book_service import BookService
from app.database.service.database_instance import get_database
from app.user.schema.user_schema import UserSchema
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
async def get_template(database: Session = Depends(get_database),
                       current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[BookSchema]:
    try:
        return BookService.get_my_books(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/preview', response_model=dict, tags=['books'])
async def preview(preview_schema: PreviewSchema,
                  current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        return {'url': BookService.preview_html(preview_schema.html, current_user)}
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