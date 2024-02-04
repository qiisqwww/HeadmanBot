from typing import TYPE_CHECKING, TypeAlias

from asyncpg import create_pool
from asyncpg.pool import Pool

from ..config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

__all__ = [
    "get_postgres_pool",
]

if TYPE_CHECKING:
    from asyncpg import Record
    DatabasePool: TypeAlias = Pool[Record]
else:
    DatabasePool: TypeAlias = Pool

async def get_postgres_pool() -> DatabasePool:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    if not hasattr(get_postgres_pool, "pool"):
        get_postgres_pool.pool = await create_pool(DATABASE_URL)
    return get_postgres_pool.pool
