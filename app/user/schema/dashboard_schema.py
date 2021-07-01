from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.user.model.dashboard_model import DashboardModel


class DashboardSchema(BaseModel):
    user_id: int
    like: int
    sub: int
    follower: int
    date: datetime

    @staticmethod
    def from_model(data: DashboardModel) -> DashboardSchema:
        return DashboardSchema(user_id=data.user_id,
                               like=data.like,
                               sub=data.sub,
                               follower=data.follower,
                               date=data.date)
