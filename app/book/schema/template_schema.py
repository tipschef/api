from __future__ import annotations

from pydantic.main import BaseModel


class TemplateSchema(BaseModel):
    content: str
    filename: str

    @staticmethod
    def from_content_and_filename(content, filename) -> TemplateSchema:
        return TemplateSchema(content=content,
                              filename=filename)
