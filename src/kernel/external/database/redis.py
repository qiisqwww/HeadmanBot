from redis.asyncio import ConnectionPool

from ...config import NKernelConfig

__all__ = [
    "get_redis_pool",
]


def get_redis_pool() -> ConnectionPool:
    config = NKernelConfig()
    host = config.REDIS_HOST
    port = config.REDIS_PORT

    redis_url = f"redis://{host}:{port}?decode_responses=True"
    if not hasattr(get_redis_pool, "pool"):
        get_redis_pool.pool = ConnectionPool().from_url(redis_url)  # type: ignore
    return get_redis_pool.pool  # type: ignore
