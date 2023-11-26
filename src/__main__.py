import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.auth.handlers import (
    registration_callbacks_router,
    registration_commands_router,
    registration_finite_state_router,
)
from src.config import BOT_TOKEN, configurate_logger
from src.database import get_pool, init_database

# from src.jobs import SendingJob, UpdateDatabaseJob
from src.middlewares import ThrottlingMiddleware


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=MemoryStorage(),
        pool=await get_pool(),
        bot=bot,
    )

    dp.include_routers(
        registration_commands_router,
        registration_callbacks_router,
        registration_finite_state_router,
        # verification_callback_router,
        # getstat_callback_router,
        # registration_router,
        # headman_router,
        # void_router,
        # faq_router,
    )

    configurate_logger()

    await init_database()

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    # sender = SendingJob(bot)
    # database_updater = UpdateDatabaseJob()
    #
    # database_updater.start()
    # sender.start()

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")


if __name__ == "__main__":
    asyncio.run(main())
