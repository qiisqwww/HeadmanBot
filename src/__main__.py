import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.config import DEBUG, LOGGING_PATH
from src.database import get_pool, init_database
from src.enums import UniversityId
from src.handlers import (
    getstat_callback_router,
    verification_callback_router,
    headman_router,
    void_router,
    registration_router,
    faq_router
)
from src.jobs import SendingJob, UpdateDatabaseJob
from src.middlewares import ThrottlingMiddleware
from src.services import UniversityService
from src.init_bot import bot


def init_logger() -> None:
    logger.add(
        LOGGING_PATH,
        compression="zip",
        rotation="500 MB",
        enqueue=True,
        backtrace=DEBUG,
        diagnose=DEBUG,
    )


async def add_unis() -> None:
    pool = await get_pool()
    async with pool.acquire() as con:
        university_service = UniversityService(con)

        for uni in UniversityId:
            await university_service.try_create(uni.uni_name)


async def main():
    dp = Dispatcher(
        storage=MemoryStorage(),
        pool=await get_pool(),
    )

    dp.include_routers(
        verification_callback_router,
        getstat_callback_router,
        registration_router,
        headman_router,
        void_router,
        faq_router)

    init_logger()

    await init_database()
    await add_unis()

    dp.message.middleware(ThrottlingMiddleware())
    sender = SendingJob(bot)
    database_updater = UpdateDatabaseJob()

    database_updater.start()
    sender.start()

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")


if __name__ == "__main__":
    asyncio.run(main())
