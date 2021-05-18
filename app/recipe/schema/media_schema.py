from pydantic import BaseModel


class MediaSchema(BaseModel):
    path: str
    media_category_id: int
