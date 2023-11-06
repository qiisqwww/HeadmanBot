import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.jobs.update_schedule_job import UpdateScheduleJob
from src.services.university_service import UniversityService

from .config import BOT_TOKEN, LOGGING_PATH
from .database import init_database
from .handlers import (
    callback_router,
    headman_reg_router,
    headman_router,
    personal_chat_router,
)
from .jobs import SendingJob, UpdateDatabaseJob


def init_logger() -> None:
    logging.basicConfig(
        filename=LOGGING_PATH,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )


async def add_unis() -> None:
    async with UniversityService() as university_service:
        for uni in ["РТУ МИРЭА"]:
            await university_service.create(uni)


async def main():
    bot = Bot(BOT_TOKEN)

    dp = Dispatcher(storage=MemoryStorage())  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(
        personal_chat_router,
        headman_reg_router,
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

    logging.info("bot is starting")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logging.info("bot was turned off")
