from abc import ABC, abstractmethod
from typing import List, AsyncGenerator
from .models import Tick

class MarketDataProvider(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def subscribe(self, symbols: List[str]):
        pass

    @abstractmethod
    async def unsubscribe(self, symbols: List[str]):
        pass

    @abstractmethod
    async def stream_ticks(self) -> AsyncGenerator[Tick, None]:
        yield # type: ignore
