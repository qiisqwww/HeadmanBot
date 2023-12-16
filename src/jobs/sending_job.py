import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from src.config import DEBUG
from src.resources import attendance_buttons
from src.resources import POLL_MESSAGE
from src.dto import Group
from src.services import (
    GroupService,
    LessonService,
    StudentService
)

__all__ = [
    "SendingJob",
]


class SendingJob:
    """Send everyone message which allow user to choose lessons which will be visited."""

    _scheduler: AsyncIOScheduler

    def __init__(
            self,
            bot: Bot,
            lesson_service: LessonService,
            student_service: StudentService,
            group_service: GroupService
    ) -> None:

        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if not DEBUG:
            self._scheduler.add_job(
                self._send,
                args=(bot,),  # IDK what should i add in args here, cuz i dont know how do we debug
            )
        else:

            self._scheduler.add_job(
                self._send,
                "cron",
                day_of_week="mon-sat",
                hour=7,
                minute=00,
                args=(
                    bot,
                    lesson_service,
                    student_service,
                    group_service
                    )
            )

    def start(self):
        self._scheduler.start()

    @logger.catch
    async def _send_to_group(
            self,
            bot: Bot,
            lesson_service: LessonService,
            student_service: StudentService,
            group: Group
    ) -> None:

        lessons = await lesson_service.filter_by_group_id(group.id)

        if not lessons:
            return

        users = await student_service.filter_by_group_id(group.id)

        for user in users:
            try:
                await bot.send_message(
                    user.telegram_id,
                    POLL_MESSAGE,
                    reply_markup=attendance_buttons(lessons)
                )
            except TelegramForbiddenError as e:
                logger.error(f"Failed to send message to user {user.surname} {user.surname} id={user.telegram_id}")
                logger.error(e)

    @logger.catch
    async def _send(
            self,
            bot: Bot,
            lesson_service: LessonService,
            student_service: StudentService,
            group_service: GroupService
    ) -> None:

        logger.info("Sending job started.")

        if DEBUG:
            await asyncio.sleep(5)

        groups = await group_service.all()

        for group in groups:
            await self._send_to_group(
                bot,
                lesson_service,
                student_service,
                group
            )

        logger.info("Sending job finished.")
