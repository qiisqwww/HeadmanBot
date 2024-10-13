import asyncio
from typing import TYPE_CHECKING

from asyncpg import create_pool, Record
from asyncpg.pool import Pool

from src.common.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
)

if TYPE_CHECKING:
    type DatabaseConnectionPool = Pool[Record]
else:
    type DatabaseConnectionPool = Pool

__all__ = [
    "create_db_pool",
]

def create_db_pool()  -> DatabaseConnectionPool:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(create_pool(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"))