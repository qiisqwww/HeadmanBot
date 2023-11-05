import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .callbacks import callback_router
from .commands import headman_router, headmen_reg_router, personal_chat_router
from .config import BOT_TOKEN, LOGGING_PATH
from .jobs import SendingJob, UpdateDatabaseJob
from .services import UsersService


def init_logger() -> None:
    logging.basicConfig(
        filename=LOGGING_PATH,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
    )  # Указываем файл для логирования


async def main():
    bot = Bot(BOT_TOKEN)  # Получаем токенstorage бота из файла с конфигом

    dp = Dispatcher(storage=MemoryStorage())  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(
        personal_chat_router,
        headmen_reg_router,
        callback_router,
        headman_router,
    )  # Добавляем роутеры в диспатчер

    init_logger()

    with UsersService() as con:
        con.create_table()

    sender = SendingJob(bot)
    updater = UpdateDatabaseJob()

    sender.start()
    updater.start()

    logging.info("bot is starting")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logging.info("bot was turned off")
