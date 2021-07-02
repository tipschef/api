import uuid
from dataclasses import dataclass
from io import BytesIO
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.book.exception.book_service_exception import BookIdNotFoundException, UniqueIdDoesNotMatch, \
    CannotModifyOthersPeopleBookException, AlreadyHaveBookException
from app.book.repository.book_purchase_repository import BookPurchaseRepository
from app.book.repository.book_recipe_repository import BookRecipeRepository
from app.book.repository.book_repository import BookRepository
from app.book.schema.book_broker_schema import BookBrokerSchema
from app.book.schema.book_purchase_schema import BookPurchaseSchema
from app.book.schema.book_schema import BookSchema
from app.book.schema.create_book_schema import CreateBookSchema
from app.book.schema.template_list_schema import TemplateListSchema
from app.book.schema.template_schema import TemplateSchema
from app.common.model.pdf import PDF
from app.common.service.broker_manager_service import get_broker_manager_service
from app.common.service.bucket_manager_service import get_bucket_manager_service
from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.service.payment_service import get_payment_service
from app.recipe.repository.media.media_repository import MediaRepository
from app.recipe.repository.recipe.recipe_repository import RecipeRepository
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_simple_schema import RecipeSimpleSchema
from app.user.repository.user_repository import UserRepository
from app.user.schema.user.user_schema import UserSchema


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

        _ = [BookRecipeRepository.create_book_recipe(database, book_model.id, recipe_template.recipe_id) for
             recipe_template in
             create_book_schema.recipe_template]

        broker.publish(
            BookBrokerSchema.from_book_schema_and_id(create_book_schema, book_model.id, current_user.username,
                                                     u_id).json())

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
            arr.append(BookSchema.from_book_model_and_number_of_recipe(book,
                                                                       BookRecipeRepository.get_number_recipe_by_book(
                                                                           database, book.id)))

        return arr

    @staticmethod
    def delete_a_book_by_id(database: Session, book_id: int, current_user: UserSchema):
        book = BookRepository.get_book_by_id(database, book_id)

        if book is None:
            raise BookIdNotFoundException()

        if book.creator_id != current_user.id:
            raise CannotModifyOthersPeopleBookException()

        BookRepository.delete_book_by_id(database, book_id)

    @staticmethod
    def get_book_by_recipe(database: Session, recipe_id: int) -> List[BookSchema]:
        books = [i[0] for i in BookRepository.get_book_by_recipe_id(database, recipe_id)]
        book_schema = []

        for book in books:
            recipes = [i[0] for i in RecipeRepository.get_recipe_by_book_id(database, book.id)]
            recipe_schemas = [RecipeSimpleSchema.from_recipe_model(i) for i in recipes]

            book_schema.append(BookSchema.from_book_model_and_recipes(book, recipe_schemas))

        return book_schema

    @staticmethod
    def get_book_by_creator(database: Session, username: str) -> List[BookSchema]:
        user = UserRepository.get_user_by_username(username)
        books = BookRepository.get_book_by_creator_id(database, user.id)
        book_schema = []

        for book in books:
            recipes = [i[0] for i in RecipeRepository.get_recipe_by_book_id(database, book.id)]
            recipe_schemas = [RecipeSimpleSchema.from_recipe_model(i) for i in recipes]

            book_schema.append(BookSchema.from_book_model_and_recipes(book, recipe_schemas))

        return book_schema

    @staticmethod
    def get_book_by_id(database: Session, book_id: int) -> BookSchema:
        book = BookRepository.get_book_by_id(database, book_id)

        recipes = [i[0] for i in RecipeRepository.get_recipe_by_book_id(database, book.id)]

        recipe_schemas = [RecipeSimpleSchema.from_recipe_model_with_thumbnail(i, MediaSchema.from_media_model(
            MediaRepository.get_media_by_id(database, i.thumbnail_id))) for i in recipes]

        return BookSchema.from_book_model_and_recipes(book, recipe_schemas)

    @staticmethod
    def buy_book_by_id(database: Session, book_id: int, user: UserSchema) -> None:
        book = BookRepository.get_book_by_id(database, book_id)

        if book is None:
            raise BookIdNotFoundException()
        purchase = BookPurchaseRepository.find_purchase_by_user_id_and_book_id(database, user.id, book_id)
        if purchase is not None:
            raise AlreadyHaveBookException()

        get_payment_service().create_payment_intent(database, user,
                                                    PaymentIntentSchema(amount=int(book.price_euro * 100)))
        BookPurchaseRepository.create_purchase(database, book_id, user.id)

    @staticmethod
    def get_book_purchase_history_by_user(database: Session, user: UserSchema) -> List[BookPurchaseSchema]:
        response = (BookPurchaseRepository.get_purchase_by_user_id(database, user.id))

        return [BookPurchaseSchema.from_model(x[0], x[1], UserRepository.get_user_by_id(x[0].user_id)) for x in response]

    @staticmethod
    def check_already_bought(database: Session, user: UserSchema, book_id: int) -> bool:
        purchase = BookPurchaseRepository.find_purchase_by_user_id_and_book_id(database, user.id, book_id)
        return purchase is not None
