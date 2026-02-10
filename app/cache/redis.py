import json
import redis.asyncio as redis
from typing import Any, Optional
from .base import Cache


class RedisCache(Cache):
    """
    Redis-backed cache implementation.

    Handles idempotency, persona caching,
    CAC tracking, and cooldown management.
    """

    def __init__(self, url: str):
        """
        Initialize Redis client.

        :param url: Redis connection URL
        """

        self.client = redis.from_url(url, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieve value from Redis.

        :param key: Cache key
        :return: Deserialized value or None
        """
        value = await self.client.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: int | None = None):
        """
        Store value in Redis.

        :param key: Cache key
        :param value: Value to store
        :param ttl: Optional expiration in seconds
        """
        data = json.dumps(value)
        if ttl:
            await self.client.setex(key, ttl, data)
        else:
            await self.client.set(key, data)

    async def incr(self, key: str, amount: int = 1, ttl: int | None = None) -> int:
        """
        Atomically increment a Redis key.

        :param key: Cache key
        :param amount: Increment amount
        :param ttl: Optional expiration
        :return: Updated value
        """
        val = await self.client.incrby(key, amount)
        if ttl:
            await self.client.expire(key, ttl)
        return val