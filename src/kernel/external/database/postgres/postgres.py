import asyncpg
from asyncpg.pool import Pool

from src.modules.university.api.contract import UniversityContract

from .config import DATABASE_URL

__all__ = [
    "init_postgres_database",
    "get_postgres_pool",
]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


async def get_postgres_pool() -> Pool:
    if not hasattr(get_postgres_pool, "pool"):
        get_postgres_pool.pool = await asyncpg.create_pool(DATABASE_URL, min_size=1)  # type: ignore
    return get_postgres_pool.pool  # type: ignore


async def init_postgres_database() -> None:
    pool = await get_postgres_pool()

    with open("src/database/create_tables.sql") as query_file:
        query = query_file.read()

    async with pool.acquire() as con:
        await con.execute(query)

        university_service = UniversityContract(con)
        await university_service.add_universities()
