import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from callbacks import router as callback_router
from config import BOT_TOKEN
from headman_commands import router as headmen_cmd_router
from headman_reg_commands import router as headmen_reg_router
from personal_chat_commands import router as personal_chat_router
from poll import router as poll_router
from sending_scheduler import SendingScheduler
from services import UsersService

LOGGING_PATH = Path("logs/logs.log")


def init_logger() -> None:
    if not LOGGING_PATH.parent.exists():
        LOGGING_PATH.parent.mkdir()

    logging.basicConfig(
        filename=LOGGING_PATH,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )  # Указываем файл для логирования


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(BOT_TOKEN)  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(
        personal_chat_router,
        headmen_reg_router,
        poll_router,
        callback_router,
        headmen_cmd_router,
    )  # Добавляем роутеры в диспетчер

    init_logger()

    with UsersService() as con:
        con.create_table()

    scheduler = SendingScheduler(bot)
    scheduler.start()

    logging.info("bot is starting")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logging.info("bot was turned off")


if __name__ == "__main__":
    asyncio.run(main())
