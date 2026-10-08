from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Tick(BaseModel):
    symbol: str
    price: Decimal
    timestamp: datetime
    source: str
    quantity: Decimal | None = None
    volume: Decimal | None = None
    instrument_id: str | None = None

class Candle(BaseModel):
    symbol: str
    timeframe: str
    start_time: datetime
    end_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    tick_count: int
    is_closed: bool
