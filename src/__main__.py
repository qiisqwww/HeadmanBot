from src.kernel import init_kernel
from src.modules.student.api.contracts import FindStudentContract

init_kernel(FindStudentContract)

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.kernel.config import BOT_TOKEN, configurate_logger

# from src.jobs import SendingJob, UpdateDatabaseJob
from src.kernel.external.database import get_postgres_pool
from src.kernel.router import Router
from src.modules.student.api.controller import student_router
from src.modules.university.api.contract import UniversityContract


async def init_postgres_database() -> None:
    pool = await get_postgres_pool()
    async with pool.acquire() as con:
        await UniversityContract(con).add_universities()


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=MemoryStorage(),
        bot=bot,
    )

    root_router = Router(throttling=True)
    root_router.include_routers(student_router)

    dp.include_router(root_router)

    configurate_logger()
    await init_postgres_database()

    # sender = SendingJob(bot)
    # database_updater = UpdateDatabaseJob()
    #
    # database_updater.start()
    # sender.start()

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")


if __name__ == "__main__":
    asyncio.run(main())
