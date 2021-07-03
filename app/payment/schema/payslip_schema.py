from datetime import datetime

from pydantic import BaseModel


class PayslipSchema(BaseModel):
    user_id: int
    amount: float
    created_date: datetime
