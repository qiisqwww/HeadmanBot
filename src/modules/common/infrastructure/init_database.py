from loguru import logger

from src.modules.common.infrastructure.database import get_postgres_pool
from src.modules.edu_info.application.commands import InsertUniversitiesCommand
from src.modules.edu_info.infrastructure.persistence import UniversityRepositoryImpl

__all__ = [
    "init_database",
]


async def init_database() -> None:
    logger.info("Start initalizing database.")
    pool = await get_postgres_pool()

    async with pool.acquire() as con:
        insert_universities_command = InsertUniversitiesCommand(UniversityRepositoryImpl(con))
        await insert_universities_command.execute()
    logger.info("Finish initalizing database.")
