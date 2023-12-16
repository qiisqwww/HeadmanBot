import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger
from asyncpg.pool import Pool

from src.config import BOT_TOKEN, configurate_logger

from src.jobs import SendingJob, UpdateDatabaseJob
from src.external.database import get_postgres_pool
from src.handlers import root_router
from src.repositories.impls import UniversityRepositoryImpl
from src.services.impls import UniversityServiceImpl


async def init_postgres_database(pool: Pool) -> None:
    async with pool.acquire() as con:
        await UniversityServiceImpl(UniversityRepositoryImpl(con)).add_universities()


async def init_jobs(bot: Bot, pool: Pool) -> None:
    sender = SendingJob(bot, pool)
    database_updater = UpdateDatabaseJob(pool)

    await database_updater.start()
    await sender.start()


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=MemoryStorage(),
        bot=bot,
    )

    dp.include_router(root_router)

    configurate_logger()

    pool = await get_postgres_pool()
    await init_postgres_database(pool)
    await init_jobs(bot, pool)

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")


if __name__ == "__main__":
    asyncio.run(main())
