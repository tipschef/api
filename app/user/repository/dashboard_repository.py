from dataclasses import dataclass
import datetime as dt
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.user.model.dashboard_model import DashboardModel


@dataclass
class DashboardRepository:

    @staticmethod
    def create_entry(database: Session, element: DashboardModel) -> DashboardModel:
        database.add(element)
        database.commit()
        database.refresh(element)
        return element

    @staticmethod
    def get_dashboard_from_partner(database: Session, user_id: int) -> List[DashboardModel]:
        return database.query(DashboardModel).filter(DashboardModel.user_id == user_id)\
            .filter(DashboardModel.date >= (datetime.now() - dt.timedelta(days=7)))\
            .all()
