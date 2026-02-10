import os
from .redis import RedisCache
from .memory import InMemoryCache


async def get_cache():
    """
    Return cache implementation.

    Priority:
    1. Redis (if REDIS_URL is set and reachable)
    2. In-memory fallback

    :return: Cache instance
    """
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        try:
            cache = RedisCache(redis_url)
            await cache.get("healthcheck")
            return cache
        except Exception:
            pass
    return InMemoryCache()