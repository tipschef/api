from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy.orm import Session

from app.user.model.tier_model import TierModel


@dataclass
class TierRepository:

    @staticmethod
    def get_tier(database: Session, tier_number: int) -> Optional[TierModel]:
        return database.query(TierModel).filter(TierModel.tier == tier_number).first()

    @staticmethod
    def get_tiers(database: Session) -> List[TierModel]:
        return database.query(TierModel).all()


