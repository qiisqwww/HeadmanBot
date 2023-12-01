from redis.asyncio import ConnectionPool

from src.config import REDIS_HOST, REDIS_PORT

__all__ = [
    "get_redis_pool",
]


def get_redis_pool() -> ConnectionPool:
    redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"
    if not hasattr(get_redis_pool, "pool"):
        get_redis_pool.pool = ConnectionPool().from_url(redis_url)  # type: ignore
    return get_redis_pool.pool  # type: ignore
