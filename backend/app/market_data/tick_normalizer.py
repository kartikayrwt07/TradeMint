from .models import Tick
from datetime import datetime
from decimal import Decimal

class TickNormalizer:
    @staticmethod
    def normalize(raw_data: dict, source: str) -> Tick:
        price = raw_data.get("price") or raw_data.get("last_price") or raw_data.get("ltp")
        if price is None:
            raise ValueError("Price missing in raw tick data")
        
        timestamp = raw_data.get("timestamp")
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be timezone-aware datetime")
            
        return Tick(
            symbol=str(raw_data.get("symbol", "")).upper(),
            price=Decimal(str(price)),
            timestamp=timestamp,
            source=source,
            quantity=Decimal(str(raw_data.get("quantity", 0))),
            volume=Decimal(str(raw_data.get("volume", 0))),
            instrument_id=raw_data.get("instrument_id")
        )
