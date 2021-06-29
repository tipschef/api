from __future__ import annotations

from app.book.schema.create_book_schema import CreateBookSchema


class BookBrokerSchema(CreateBookSchema):
    id: int
    author_name: str
    u_id: str

    @staticmethod
    def from_book_schema_and_id(create_book_schema: CreateBookSchema, book_id: id, author_name: str,
                                u_id: str) -> BookBrokerSchema:
        return BookBrokerSchema(name=create_book_schema.name,
                                description=create_book_schema.description,
                                cover_path=create_book_schema.cover_path,
                                description_path=create_book_schema.description_path,
                                cover_picture_path=create_book_schema.cover_picture_path,
                                recipe_template=create_book_schema.recipe_template,
                                id=book_id,
                                author_name=author_name,
                                u_id=u_id
                                )
