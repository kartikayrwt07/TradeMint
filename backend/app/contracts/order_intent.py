from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from decimal import Decimal

class OrderIntent(BaseModel):
    strategy_id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: int
    order_type: Literal["MARKET", "LIMIT"]
    signal_id: str
    created_at: datetime
    reason: str
    reference_price: Decimal | None = None
