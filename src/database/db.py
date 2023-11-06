import asyncpg
from asyncpg.connection import Connection

from .config import DATABASE_URL

__all__ = [
    "get_db_connection",
    "init_database",
]


async def get_db_connection() -> Connection:
    conn = await asyncpg.connect(DATABASE_URL)
    return conn


async def init_database() -> None:
    conn = await get_db_connection()

    with open("src/database/create_tables.sql") as query_file:
        query = query_file.read()
    await conn.execute(query)

    await conn.close()
