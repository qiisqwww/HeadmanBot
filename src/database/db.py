import asyncpg
from asyncpg.connection import Connection

from .config import DATABASE_URL

__all__ = [
    "get_db_connection",
]


async def get_db_connection() -> Connection:
    conn = await asyncpg.connect(DATABASE_URL)
    return conn
