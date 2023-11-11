from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.config import BOT_TOKEN, DEBUG, LOGGING_PATH
from src.database import get_pool, init_database
from src.handlers import (
    callback_router,
    headman_registration_router,
    headman_router,
    student_registration_router,
)
from src.jobs import SendingJob, UpdateDatabaseJob, UpdateScheduleJob
from src.mirea_api import MireaScheduleApi
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
    university_service = UniversityService(await pool.acquire())
    for uni in ["РТУ МИРЭА"]:
        await university_service.create(uni)


async def main():
    dp = Dispatcher(storage=MemoryStorage(), pool=await get_pool(), api=MireaScheduleApi())
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
    updater = UpdateDatabaseJob()
    schedule_updater = UpdateScheduleJob()

    # schedule_updater.start()
    updater.start()
    # sender.start()

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")
