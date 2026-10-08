from abc import ABC, abstractmethod
from typing import List
from ..market_data.models import Candle
from ..contracts.trading_signal import TradingSignal
import uuid
from datetime import datetime

class BaseStrategy(ABC):
    def __init__(self, strategy_id: str, name: str, symbols: List[str]):
        self.strategy_id = strategy_id
        self.name = name
        self.symbols = symbols
        self.status = "STOPPED"
        self.signals: List[TradingSignal] = []
        self.history: dict[str, List[Candle]] = {sym: [] for sym in symbols}

    def initialize(self):
        self.status = "STARTING"
        self.status = "RUNNING"

    def stop(self):
        self.status = "STOPPING"
        self.status = "STOPPED"

    def fail(self):
        self.status = "FAILED"

    def reset(self):
        self.history = {sym: [] for sym in self.symbols}
        self.signals = []

    def on_candle(self, candle: Candle) -> TradingSignal | None:
        if self.status != "RUNNING" or candle.symbol not in self.symbols:
            return None
        self.history[candle.symbol].append(candle)
        if len(self.history[candle.symbol]) > 1000:
            self.history[candle.symbol].pop(0)
            
        return self.evaluate(candle.symbol)

    @abstractmethod
    def evaluate(self, symbol: str) -> TradingSignal | None:
        pass

    def get_state(self):
        return {
            "strategy_id": self.strategy_id,
            "status": self.status,
            "history_lengths": {s: len(self.history[s]) for s in self.symbols}
        }
        
    def _create_signal(self, symbol: str, side: str, reference_price: Decimal, reason: str, timeframe: str) -> TradingSignal:
        sig = TradingSignal(
            signal_id=str(uuid.uuid4()),
            strategy_id=self.strategy_id,
            symbol=symbol,
            side=side,
            timestamp=datetime.now(),
            reference_price=reference_price,
            reason=reason,
            timeframe=timeframe
        )
        self.signals.append(sig)
        return sig
