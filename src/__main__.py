import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

# from src.jobs import SendingJob, UpdateDatabaseJob
from src.config import BOT_TOKEN, configurate_logger
from src.database import init_postgres_database
from src.modules.student.api.controller import student_router
from src.shared.middlewares import (
    InjectDBConnectionMiddleware,
    InjectRedisConnectionMiddleware,
    ThrottlingMiddleware,
)


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=MemoryStorage(),
        bot=bot,
    )

    dp.include_routers(
        student_router,
        # verification_callback_router,
        # getstat_callback_router,
        # registration_router,
        # headman_router,
        # faq_router,
    )

    # @dp.message(flags={"void": "void"})
    # async def handles_everything() -> None:
    #     pass

    configurate_logger()

    await init_postgres_database()

    dp.message.outer_middleware(InjectRedisConnectionMiddleware())
    dp.message.outer_middleware(InjectDBConnectionMiddleware())

    dp.callback_query.outer_middleware(InjectRedisConnectionMiddleware())
    dp.callback_query.outer_middleware(InjectDBConnectionMiddleware())

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
