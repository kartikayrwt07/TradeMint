import asyncio
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from backend.app.market_data.models import Tick
from backend.app.market_data.mock_provider import MockMarketDataProvider
from backend.app.market_data.candle_engine import CandleEngine
from backend.app.strategies.strategy_manager import StrategyManager
from backend.app.strategies.strategy_a import StrategyA
from backend.app.strategies.strategy_b import StrategyB
from backend.app.strategies.strategy_c import StrategyC

async def main():
    print("TradeMint Strategy Engine - Local Demo")
    base_time = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    
    ticks = []
    for i in range(30):
        price = Decimal("100") + Decimal(i * 2) 
        ts = base_time + timedelta(minutes=i)
        ticks.append(Tick(symbol="RELIANCE", price=price, timestamp=ts, source="MOCK"))

    provider = MockMarketDataProvider(ticks)
    await provider.connect()
    await provider.subscribe(["RELIANCE"])

    manager = StrategyManager()
    manager.register(StrategyA("MACross", ["RELIANCE"], 2, 5), 10)
    manager.register(StrategyB("Mom", ["RELIANCE"], 3, 0.05), 20)
    manager.register(StrategyC("Break", ["RELIANCE"], 3), 30)
    manager.start_all()

    engine = CandleEngine([manager.on_candle_closed])

    print("Streaming ticks...")
    async for tick in provider.stream_ticks():
        engine.process_tick(tick)
    
    engine.flush()
    
    print("--- GENERATED INTENTS ---")
    for intent in manager.intents:
        print(f"ORDER INTENT | strategy={intent.strategy_id} | symbol={intent.symbol} | side={intent.side} | qty={intent.quantity} | reason={intent.reason}")

if __name__ == "__main__":
    asyncio.run(main())\n