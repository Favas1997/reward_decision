import time
from typing import Any, Optional
from .base import Cache


class InMemoryCache(Cache):
    """
    Simple in-memory cache implementation.

    Intended for local development and testing.
    """

    def __init__(self):
        self.store = {}

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from memory cache.

        :param key: Cache key
        :return: Cached value or None
        """
        item = self.store.get(key)
        if not item:
            return None

        value, expiry = item
        if expiry and expiry < time.time():
            del self.store[key]
            return None
        return value
    

    async def set(self, key: str, value: Any, ttl: int | None = None):
        """
        Store value in memory cache.

        :param key: Cache key
        :param value: Value to store
        :param ttl: Optional expiration in seconds
        """
        expiry = time.time() + ttl if ttl else None
        self.store[key] = (value, expiry)
    

    async def incr(self, key: str, amount: int = 1, ttl: int | None = None) -> int:
        """
        Increment a numeric value in memory cache.

        :param key: Cache key
        :param amount: Increment amount
        :param ttl: Optional expiration
        :return: Updated value
        """
        current = await self.get(key) or 0
        new_val = current + amount
        await self.set(key, new_val, ttl)
        return new_val