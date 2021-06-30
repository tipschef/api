from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.user.model.tier_model import TierModel


@dataclass
class TierRepository:

    @staticmethod
    def get_tier(database: Session, tier_number: int) -> Optional[TierModel]:
        return database.query(TierModel).filter(TierModel.tier == tier_number).first()
