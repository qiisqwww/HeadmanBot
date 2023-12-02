import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

# from src.jobs import SendingJob, UpdateDatabaseJob
from src.config import (
    BOT_TOKEN,
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
    REDIS_HOST,
    REDIS_PORT,
    configurate_logger,
)
from src.kernel import NKernelConfig
from src.kernel.external.database import get_postgres_pool
from src.modules.student.api.controller import student_router
from src.modules.university.api.contract import UniversityContract


async def main():
    NKernelConfig.initialize(
        postgres_user=DB_USER,
        postgres_pass=DB_PASS,
        postgres_name=DB_NAME,
        postgres_host=DB_HOST,
        postgres_port=DB_PORT,
        redis_host=REDIS_HOST,
        redis_port=REDIS_PORT,
        debug=DEBUG,
    )

    pool = await get_postgres_pool()
    async with pool.acquire() as con:
        await UniversityContract(con).add_universities()

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

    # await init_postgres_database()

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
