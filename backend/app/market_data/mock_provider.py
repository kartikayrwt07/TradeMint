import asyncio
from typing import List, AsyncGenerator
from .interfaces import MarketDataProvider
from .models import Tick

class MockMarketDataProvider(MarketDataProvider):
    def __init__(self, predefined_ticks: List[Tick] = None):
        self.predefined_ticks = predefined_ticks or []
        self.subscribed_symbols = set()
        self.is_connected = False

    async def connect(self):
        self.is_connected = True

    async def disconnect(self):
        self.is_connected = False

    async def subscribe(self, symbols: List[str]):
        self.subscribed_symbols.update(symbols)

    async def unsubscribe(self, symbols: List[str]):
        for s in symbols:
            if s in self.subscribed_symbols:
                self.subscribed_symbols.remove(s)

    async def stream_ticks(self) -> AsyncGenerator[Tick, None]:
        for tick in self.predefined_ticks:
            if not self.is_connected:
                break
            if tick.symbol in self.subscribed_symbols:
                yield tick
                await asyncio.sleep(0.001)
