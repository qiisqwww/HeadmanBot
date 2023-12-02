import asyncpg
from asyncpg.pool import Pool

from ...config import NKernelConfig

__all__ = [
    "get_postgres_pool",
]


async def get_postgres_pool() -> Pool:
    config = NKernelConfig()

    user = config.POSTGRES_USER
    password = config.POSTGRES_PASS
    host = config.POSTGRES_HOST
    name = config.POSTGRES_NAME
    port = config.POSTGRES_PORT

    DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

    if not hasattr(get_postgres_pool, "pool"):
        get_postgres_pool.pool = await asyncpg.create_pool(DATABASE_URL, min_size=1)  # type: ignore
    return get_postgres_pool.pool  # type: ignore
