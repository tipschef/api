from __future__ import annotations

from pydantic.main import BaseModel


class PreviewSchema(BaseModel):
    html: str
