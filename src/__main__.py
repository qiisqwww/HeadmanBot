import asyncio

from loguru import logger

from src.bot import bot, dispatcher
from src.modules.common.infrastructure import DEBUG, configurate_logger, init_database

# async def init_jobs(bot: Bot, pool: Pool) -> None:
#     sender = SendingJob(bot, pool)
#     database_updater = UpdateDatabaseJob(pool)
#
#     await database_updater.start()
#     await sender.start()


async def start_debug_bot() -> None:
    logger.info("Bot starting.")
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)
    logger.info("Bot stoped.")


async def main() -> None:
    configurate_logger()

    await init_database()

    if DEBUG:
        await start_debug_bot()

    # await init_jobs(bot, pool)


if __name__ == "__main__":
    asyncio.run(main())
