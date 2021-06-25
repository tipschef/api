from pydantic import BaseModel


class CommentInputSchema(BaseModel):
    content: str
