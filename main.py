import asyncio
import logging
import schedule
from request import restart_schedule, threat
from aiogram import Dispatcher, Bot, types
from aiogram.fsm.storage.memory import MemoryStorage

from personal_chat_commands import router as personal_chat_router
from config.config_reader import config
from service import UsersService


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(config.BOT_TOKEN.get_secret_value())  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(personal_chat_router)  # Добавляем роутеры в диспетчер
    logging.basicConfig(filename='logs/logs.logs', level=logging.DEBUG)  # Указываем файл для логирования
    schedule.every().day.at("06:50").do(restart_schedule, bot=bot)  # рассылка уведомлений
    with UsersService() as con:
        con.create_table()

    logging.info('bot is starting')
    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота
    restart_schedule(bot)
    threat()



    @dp.callback_query(func=lambda c: c.data == 'button1')
    async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

if __name__ == '__main__':
    asyncio.run(main())
