from .base_strategy import BaseStrategy
from .indicators import sma
from ..contracts.trading_signal import TradingSignal

class StrategyA(BaseStrategy):
    def __init__(self, strategy_id: str, symbols: list[str], fast_period: int = 5, slow_period: int = 20):
        super().__init__(strategy_id, "Moving Average Crossover", symbols)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def evaluate(self, symbol: str) -> TradingSignal | None:
        candles = self.history[symbol]
        if len(candles) < self.slow_period + 1:
            return None

        closes = [c.close for c in candles]
        
        current_fast = sma(closes, self.fast_period)
        current_slow = sma(closes, self.slow_period)
        
        prev_fast = sma(closes[:-1], self.fast_period)
        prev_slow = sma(closes[:-1], self.slow_period)

        if current_fast and current_slow and prev_fast and prev_slow:
            if prev_fast <= prev_slow and current_fast > current_slow:
                return self._create_signal(symbol, "BUY", closes[-1], "MA_CROSSOVER_UP", candles[-1].timeframe)
            elif prev_fast >= prev_slow and current_fast < current_slow:
                return self._create_signal(symbol, "SELL", closes[-1], "MA_CROSSOVER_DOWN", candles[-1].timeframe)
        return None
