from typing import Any, AsyncGenerator

from redis.asyncio import ConnectionPool, Redis

from ..config import REDIS_HOST, REDIS_PORT

__all__ = [
    "get_redis_connection",
]


def get_redis_pool() -> ConnectionPool:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"

    if not hasattr(get_redis_pool, "pool"):
        get_redis_pool.pool = ConnectionPool().from_url(REDIS_URL)  # type: ignore
    return get_redis_pool.pool  # type: ignore


async def get_redis_connection() -> AsyncGenerator[Redis, Any]:
    pool = get_redis_pool()

    async with Redis(connection_pool=pool) as con:
        yield con
