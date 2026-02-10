
from abc import ABC, abstractmethod
from typing import Any, Optional

class Cache(ABC):
    """
    Abstract cache interface.

    Enables cache-first design and allows swapping
    cache backends without changing business logic.
    """

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None):
        pass

    @abstractmethod
    async def incr(self, key: str, amount: int = 1, ttl: int | None = None) -> int:
        pass