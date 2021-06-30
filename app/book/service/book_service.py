import uuid
from dataclasses import dataclass
from io import BytesIO
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.book.exception.book_service_exception import BookIdNotFoundException, UniqueIdDoesNotMatch, \
    CannotModifyOthersPeopleBookException
from app.book.repository.book_recipe_repository import BookRecipeRepository
from app.book.repository.book_repository import BookRepository
from app.book.schema.book_broker_schema import BookBrokerSchema
from app.book.schema.book_schema import BookSchema
from app.book.schema.create_book_schema import CreateBookSchema
from app.book.schema.template_list_schema import TemplateListSchema
from app.book.schema.template_schema import TemplateSchema
from app.common.model.pdf import PDF
from app.common.service.broker_manager_service import get_broker_manager_service
from app.common.service.bucket_manager_service import get_bucket_manager_service
from app.user.schema.user_schema import UserSchema


@dataclass
class BookService:

    @staticmethod
    def get_templates() -> TemplateListSchema:
        book_descriptions = BookService.get_bucket_folder_content('templates/book_description/')
        cover_pages = BookService.get_bucket_folder_content('templates/cover_page/')
        recipes = BookService.get_bucket_folder_content('templates/recipe/')
        summaries = BookService.get_bucket_folder_content('templates/summary/')

        return TemplateListSchema.from_different_lists(book_descriptions, cover_pages, recipes, summaries)

    @staticmethod
    def get_bucket_folder_content(path) -> List[TemplateSchema]:
        files_content = []
        files = get_bucket_manager_service().get_list(path)
        for file in files:
            files_content.append(TemplateSchema.from_content_and_filename(file.download_as_text(), file.name))

        return files_content[1:]

    @staticmethod
    def preview_html(html: str, user: UserSchema) -> str:
        pdf = PDF()
        pdf.add_page()
        pdf.write_html(html)
        bucket = get_bucket_manager_service()
        filename = bucket.save_file(f'preview/{user.id}_{uuid.uuid4()}.pdf', BytesIO(bytes(pdf.output())))
        return filename

    @staticmethod
    def post_cover(user_id: int, cover: UploadFile) -> str:
        name = f'{user_id}/book_cover/{uuid.uuid4()}_{cover.filename}'
        filename = get_bucket_manager_service().save_file(name, cover.file)
        return filename

    @staticmethod
    def create_book(database: Session, create_book_schema: CreateBookSchema, current_user: UserSchema) -> BookSchema:
        broker = get_broker_manager_service()
        u_id = str(uuid.uuid4())
        book_model = BookRepository.create_book(database, create_book_schema, current_user.id, u_id)

        _ = [BookRecipeRepository.create_book_recipe(database, book_model.id, recipe_template.recipe_id) for recipe_template in
             create_book_schema.recipe_template]

        broker.publish(BookBrokerSchema.from_book_schema_and_id(create_book_schema, book_model.id, current_user.username, u_id).json())

        return BookSchema.from_book_model(book_model)

    @staticmethod
    def add_pdf_to_book(database: Session, book_id: int, u_id: str, file: UploadFile) -> BookSchema:
        book = BookRepository.get_book_by_id_deleted_or_not(database, book_id)
        if book is None:
            raise BookIdNotFoundException()

        if book.u_id != u_id:
            raise UniqueIdDoesNotMatch()

        filename = get_bucket_manager_service().save_file(
            f'{book.creator_id}/book/{book.id}_pdf.pdf', file.file)

        BookRepository.update_book_by_id(database, book_id, filename)

        return BookSchema.from_book_model(book)

    @staticmethod
    def get_my_books(database: Session, current_user: UserSchema) -> List[BookSchema]:
        arr = []
        books = BookRepository.get_book_by_creator_id(database, current_user.id)

        for book in books:
            arr.append(BookSchema.from_book_model_and_number_of_recipe(book, BookRecipeRepository.get_number_recipe_by_book(database, book.id)))

        return arr

    @staticmethod
    def delete_a_book_by_id(database: Session, book_id: int, current_user: UserSchema):
        book = BookRepository.get_book_by_id(database, book_id)

        if book is None:
            raise BookIdNotFoundException()

        if book.creator_id != current_user.id:
            raise CannotModifyOthersPeopleBookException()

        BookRepository.delete_book_by_id(database, book_id)








