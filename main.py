import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot, types
from aiogram.fsm.storage.memory import MemoryStorage

from personal_chat_commands import router as personal_chat_router, job
from config.config_reader import config
from service import UsersService


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(config.BOT_TOKEN.get_secret_value())  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(personal_chat_router)  # Добавляем роутеры в диспетчер
    logging.basicConfig(filename='logs/logs.logs', level=logging.DEBUG)  # Указываем файл для логирования

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(job,'interval',seconds=50 ,args=(1, bot.send_message))

    await job(1 , bot.send_message)
    scheduler.start()
    with UsersService() as con:
        con.create_table()

    logging.info('bot is starting')

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logging.info("bot was turned off")

if __name__ == '__main__':
    asyncio.run(main())
