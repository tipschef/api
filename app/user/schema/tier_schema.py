from __future__ import annotations

from pydantic import BaseModel

from app.user.model.tier_model import TierModel


class TierSchema(BaseModel):
    id: int
    tier: int
    price: float

    @staticmethod
    def from_model(tier: TierModel) -> TierSchema:
        return TierSchema(id=tier.id,
                          tier=tier.tier,
                          price=tier.price)
