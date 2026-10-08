from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from decimal import Decimal

class TradingSignal(BaseModel):
    signal_id: str
    strategy_id: str
    symbol: str
    side: Literal["BUY", "SELL"]
    timestamp: datetime
    reference_price: Decimal
    reason: str
    timeframe: str
