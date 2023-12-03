from redis.asyncio import ConnectionPool

from src.kernel.config import REDIS_HOST, REDIS_PORT

__all__ = [
    "get_redis_pool",
]


def get_redis_pool() -> ConnectionPool:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"

    if not hasattr(get_redis_pool, "pool"):
        get_redis_pool.pool = ConnectionPool().from_url(REDIS_URL)  # type: ignore
    return get_redis_pool.pool  # type: ignore
