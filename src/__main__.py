import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.config import BOT_TOKEN, DEBUG, LOGGING_PATH
from src.database import get_pool, init_database
from src.enums import UniversityId
from src.handlers import (
    callback_router,
    headman_registration_router,
    headman_router,
    student_registration_router,
)
from src.jobs import SendingJob, UpdateDatabaseJob
from src.services import UniversityService


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
        student_registration_router,
        headman_registration_router,
        callback_router,
        headman_router,
    )

    await init_database()
    await add_unis()
    init_logger()

    bot = Bot(BOT_TOKEN)

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
