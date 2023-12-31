import asyncpg
from asyncpg.pool import Pool

from ..config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

__all__ = [
    "get_postgres_pool",
]


async def get_postgres_pool() -> Pool:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    if not hasattr(get_postgres_pool, "pool"):
        get_postgres_pool.pool = await asyncpg.create_pool(DATABASE_URL)  # type: ignore
    return get_postgres_pool.pool  # type: ignore
