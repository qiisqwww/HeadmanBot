import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from src.config import BOT_TOKEN, configurate_logger

from src.jobs import SendingJob, UpdateDatabaseJob
from src.external.database import get_postgres_pool
from src.handlers import root_router
from src.repositories.impls import (
    UniversityRepositoryImpl,
    LessonRepositoryImpl,
    StudentRepositoryImpl,
    GroupRepositoryImpl,
    AttendanceRepositoryImpl
)
from src.services.impls import (
    UniversityServiceImpl,
    LessonServiceImpl,
    StudentServiceImpl,
    GroupServiceImpl,
    AttendanceServiceImpl
)


async def init_postgres_database() -> None:
    pool = await get_postgres_pool()
    async with pool.acquire() as con:
        await UniversityServiceImpl(UniversityRepositoryImpl(con)).add_universities()


async def init_jobs(bot: Bot) -> None:
    pool = await get_postgres_pool()

    async with pool.acquire() as con:
        student_service = StudentServiceImpl(StudentRepositoryImpl(con))
        group_service = GroupServiceImpl(GroupRepositoryImpl(con))
        lesson_service = LessonServiceImpl(
            LessonRepositoryImpl(con),
            group_service,
            UniversityServiceImpl(UniversityRepositoryImpl(con))
        )
        attendance_service = AttendanceServiceImpl(
            AttendanceRepositoryImpl(con),
            lesson_service,
            student_service
        )

    sender = SendingJob(
        bot,
        lesson_service,
        student_service,
        group_service
    )
    database_updater = UpdateDatabaseJob(
        lesson_service,
        attendance_service
    )

    database_updater.start()
    sender.start()


async def main():
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(
        storage=MemoryStorage(),
        bot=bot,
    )

    dp.include_router(root_router)

    configurate_logger()
    await init_postgres_database()
    await init_jobs(bot)

    logger.info("Bot is starting.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    logger.info("Bot was turned off.")


if __name__ == "__main__":
    asyncio.run(main())
