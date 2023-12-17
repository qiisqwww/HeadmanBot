import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.pool import Pool
from loguru import logger

from src.config import DEBUG
from src.dto.models import Group
from src.repositories.impls import (
    GroupRepositoryImpl,
    LessonRepositoryImpl,
    StudentRepositoryImpl,
    UniversityRepositoryImpl,
)
from src.resources import POLL_MESSAGE, attendance_buttons
from src.services import LessonService, StudentService
from src.services.impls import (
    GroupServiceImpl,
    LessonServiceImpl,
    StudentServiceImpl,
    UniversityServiceImpl,
)

__all__ = [
    "SendingJob",
]


class SendingJob:
    """Send everyone message which allow user to choose lessons which will be visited."""

    _scheduler: AsyncIOScheduler

    def __init__(self, bot: Bot, pool: Pool) -> None:
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send, args=(bot, pool))
        else:
            self._scheduler.add_job(self._send, "cron", day_of_week="mon-sat", hour=7, minute=00, args=(bot, pool))

    async def start(self):
        self._scheduler.start()

    @logger.catch
    async def _send_to_group(
        self, bot: Bot, lesson_service: LessonService, student_service: StudentService, group: Group
    ) -> None:
        lessons = await lesson_service.filter_by_group_id(group.id)

        if not lessons:
            return

        users = await student_service.filter_by_group_id(group.id)

        for user in users:
            try:
                await bot.send_message(user.telegram_id, POLL_MESSAGE, reply_markup=attendance_buttons(lessons))
            except TelegramForbiddenError as e:
                logger.error(f"Failed to send message to user {user.surname} {user.surname} id={user.telegram_id}")
                logger.error(e)

    @logger.catch
    async def _send(self, bot: Bot, pool: Pool) -> None:
        async with pool.acquire() as con:
            group_service = GroupServiceImpl(GroupRepositoryImpl(con))
            student_service = StudentServiceImpl(
                StudentRepositoryImpl(con), group_service, UniversityServiceImpl(UniversityRepositoryImpl(con))
            )
            lesson_service = LessonServiceImpl(
                LessonRepositoryImpl(con), group_service, UniversityServiceImpl(UniversityRepositoryImpl(con))
            )
            logger.info("Sending job started.")

            if DEBUG:
                await asyncio.sleep(5)

            groups = await group_service.all()

            for group in groups:
                await self._send_to_group(bot, lesson_service, student_service, group)

        logger.info("Sending job finished.")
