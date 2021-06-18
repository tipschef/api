from pydantic import BaseModel


class LikeSchema(BaseModel):
    recipe_id: int
    like_count: int
    liked_by_me: bool
