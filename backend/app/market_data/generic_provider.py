from typing import List, AsyncGenerator
from .interfaces import MarketDataProvider
from .models import Tick

class GenericMarketDataProvider(MarketDataProvider):
    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def subscribe(self, symbols: List[str]):
        pass

    async def unsubscribe(self, symbols: List[str]):
        pass

    async def stream_ticks(self) -> AsyncGenerator[Tick, None]:
        if False:
            yield None # type: ignore
