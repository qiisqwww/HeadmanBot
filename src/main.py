from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.config import BOT_TOKEN, DEBUG, LOGGING_PATH
from src.database import init_database
from src.handlers import (
    callback_router,
    headman_registration_router,
    headman_router,
    student_registration_router,
)
from src.jobs import SendingJob, UpdateDatabaseJob, UpdateScheduleJob
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
    async with UniversityService() as university_service:
        for uni in ["РТУ МИРЭА"]:
            await university_service.create(uni)


async def main():
    bot = Bot(BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(
        student_registration_router,
        headman_registration_router,
        callback_router,
        headman_router,
    )  # Добавляем роутеры в диспатчер

    await init_database()
    await add_unis()
    init_logger()

    sender = SendingJob(bot)
    updater = UpdateDatabaseJob()
    schedule_updater = UpdateScheduleJob()

    # schedule_updater.start()
    updater.start()
    sender.start()

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logger.info("Bot was turned off.")
