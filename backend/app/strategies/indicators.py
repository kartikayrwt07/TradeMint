from decimal import Decimal
from typing import List
from ..market_data.models import Candle

def sma(values: List[Decimal], period: int) -> Decimal | None:
    if len(values) < period or period <= 0:
        return None
    return sum(values[-period:]) / Decimal(period)

def ema(values: List[Decimal], period: int) -> Decimal | None:
    if len(values) < period or period <= 0:
        return None
    k = Decimal("2.0") / Decimal(period + 1)
    
    ema_val = sum(values[:period]) / Decimal(period)
    
    for price in values[period:]:
        ema_val = (price - ema_val) * k + ema_val
    return ema_val

def momentum(values: List[Decimal], period: int) -> Decimal | None:
    if len(values) <= period:
        return None
    current = values[-1]
    past = values[-(period + 1)]
    if past == 0:
        return None
    return (current / past) - Decimal("1")

def previous_high(candles: List[Candle], lookback: int) -> Decimal | None:
    if len(candles) < lookback:
        return None
    relevant = candles[-lookback:]
    return max(c.high for c in relevant)

def previous_low(candles: List[Candle], lookback: int) -> Decimal | None:
    if len(candles) < lookback:
        return None
    relevant = candles[-lookback:]
    return min(c.low for c in relevant)
