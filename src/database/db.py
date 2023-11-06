import asyncpg
from asyncpg.connection import Connection

from .config import DATABASE_URL


async def get_connection() -> Connection:
    conn = await asyncpg.connect(DATABASE_URL)
    return conn
