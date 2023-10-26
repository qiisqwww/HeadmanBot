import asyncio
import logging
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from personal_chat_commands import router as personal_chat_router
from headmen_reg_commands import router as headmen_reg_router
from headmen_commands import router as headmen_cmd_router
from poll import router as poll_router, job
from config.config_reader import config
from service import UsersService
from callbacks import router as callback_router


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(config.BOT_TOKEN.get_secret_value())  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(personal_chat_router, headmen_reg_router,
                       poll_router, callback_router, headmen_cmd_router)  # Добавляем роутеры в диспетчер

    logging.basicConfig(filename='logs/logs.logs', level=logging.DEBUG)  # Указываем файл для логирования

    with UsersService() as con:
        con.create_table()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(job,'cron', day_of_week='mon-sun', hour=7, minute=00, args=(1, bot.send_message))
    scheduler.add_job(job, 'interval', seconds=60, args=(1, bot.send_message))
    await job(1, bot.send_message)
    scheduler.start()

    logging.info('bot is starting')

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота

    logging.info("bot was turned off")

if __name__ == '__main__':
    asyncio.run(main())
