from pydantic import BaseModel


class MediaBaseSchema(BaseModel):
    path: str
    media_category_id: int
