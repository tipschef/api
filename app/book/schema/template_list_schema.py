from __future__ import annotations

from typing import List

from pydantic.main import BaseModel

from app.book.schema.template_schema import TemplateSchema


class TemplateListSchema(BaseModel):
    book_descriptions: List[TemplateSchema]
    cover_pages: List[TemplateSchema]
    recipes: List[TemplateSchema]
    summaries: List[TemplateSchema]

    @staticmethod
    def from_different_lists(book_descriptions, cover_pages, recipes, summaries) -> TemplateListSchema:
        return TemplateListSchema(book_descriptions=book_descriptions,
                                  cover_pages=cover_pages,
                                  recipes=recipes,
                                  summaries=summaries)
