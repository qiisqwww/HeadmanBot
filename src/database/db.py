import asyncpg
from asyncpg.pool import Pool

from src.bot.services import UniversityService

from .config import DATABASE_URL

__all__ = [
    "init_database",
    "get_pool",
]


async def get_pool() -> Pool:
    if not hasattr(get_pool, "pool"):
        get_pool.pool = await asyncpg.create_pool(DATABASE_URL)  # type: ignore
    return get_pool.pool  # type: ignore


async def init_database() -> None:
    pool = await get_pool()

    with open("src/database/create_tables.sql") as query_file:
        query = query_file.read()

    async with pool.acquire() as con:
        await con.execute(query)

        university_service = UniversityService(con)
        await university_service.add_universities()
