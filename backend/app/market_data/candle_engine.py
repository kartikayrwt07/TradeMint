from datetime import datetime, timedelta
from typing import Dict, List, Callable
from decimal import Decimal
from .models import Tick, Candle

class CandleClosedEvent:
    def __init__(self, candle: Candle):
        self.candle = candle
        self.symbol = candle.symbol
        self.timeframe = candle.timeframe
        self.timestamp = candle.end_time

class CandleEngine:
    def __init__(self, callbacks: List[Callable[[CandleClosedEvent], None]] = None):
        self.callbacks = callbacks or []
        self.active_candles: Dict[str, Dict[str, Candle]] = {
            "1m": {},
            "5m": {}
        }

    def process_tick(self, tick: Tick):
        self._process_tick_for_timeframe(tick, "1m", 1)
        self._process_tick_for_timeframe(tick, "5m", 5)

    def _get_bucket_start(self, dt: datetime, minutes: int) -> datetime:
        bucket_minute = (dt.minute // minutes) * minutes
        return dt.replace(minute=bucket_minute, second=0, microsecond=0)

    def _process_tick_for_timeframe(self, tick: Tick, timeframe: str, minutes: int):
        bucket_start = self._get_bucket_start(tick.timestamp, minutes)
        bucket_end_exclusive = bucket_start + timedelta(minutes=minutes)

        active = self.active_candles[timeframe].get(tick.symbol)
        
        if active and tick.timestamp >= active.end_time:
            self._close_candle(active)
            active = None

        if not active:
            active = Candle(
                symbol=tick.symbol,
                timeframe=timeframe,
                start_time=bucket_start,
                end_time=bucket_end_exclusive,
                open=tick.price,
                high=tick.price,
                low=tick.price,
                close=tick.price,
                volume=tick.volume or Decimal("0"),
                tick_count=1,
                is_closed=False
            )
            self.active_candles[timeframe][tick.symbol] = active
        else:
            active.high = max(active.high, tick.price)
            active.low = min(active.low, tick.price)
            active.close = tick.price
            active.volume += (tick.volume or Decimal("0"))
            active.tick_count += 1

    def _close_candle(self, candle: Candle):
        candle.is_closed = True
        event = CandleClosedEvent(candle)
        for cb in self.callbacks:
            cb(event)

    def flush(self):
        for tf in self.active_candles:
            for sym, candle in list(self.active_candles[tf].items()):
                self._close_candle(candle)
            self.active_candles[tf].clear()
