from .base_strategy import BaseStrategy
from .indicators import momentum
from ..contracts.trading_signal import TradingSignal

class StrategyB(BaseStrategy):
    def __init__(self, strategy_id: str, symbols: list[str], period: int = 5, threshold: float = 0.005):
        super().__init__(strategy_id, "Momentum", symbols)
        self.period = period
        self.threshold = threshold

    def evaluate(self, symbol: str) -> TradingSignal | None:
        candles = self.history[symbol]
        if len(candles) <= self.period:
            return None

        closes = [c.close for c in candles]
        mom = momentum(closes, self.period)

        if mom is not None:
            if mom >= self.threshold:
                return self._create_signal(symbol, "BUY", closes[-1], "HIGH_MOMENTUM_UP", candles[-1].timeframe)
            elif mom <= -self.threshold:
                return self._create_signal(symbol, "SELL", closes[-1], "HIGH_MOMENTUM_DOWN", candles[-1].timeframe)
        return None
