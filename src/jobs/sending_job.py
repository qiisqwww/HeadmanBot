from datetime import datetime
from typing import Callable

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.buttons import load_attendance_kb
from src.config import DEBUG
from src.messages import POLL_MESSAGE
from src.services.group_service import GroupService
from src.services.lesson_service import LessonService
from src.services.student_service import StudentService

__all__ = [
    "SendingJob",
]


class SendingJob:
    """Send everyone message which allow user to choose lessons which will be visited."""

    _scheduler: AsyncIOScheduler

    def __init__(self, bot: Bot):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(self._send, args=(bot.send_message,))
        else:
            self._scheduler.add_job(
                self._send, "cron", day_of_week="mon-sun", hour=7, minute=00, args=(bot.send_message,)
            )

    def start(self):
        self._scheduler.start()

    @staticmethod
    async def _send(poll_user: Callable):
        async with GroupService() as group_service:
            groups = await group_service.all()

        for group in groups:
            async with LessonService() as lesson_service:
                schedule = await lesson_service.get_by_group(group.id)
            schedule = tuple(filter(lambda lesson: lesson.weekday == datetime.now().weekday(), schedule))

            if schedule is None:
                continue

            async with StudentService() as student_service:
                users = await student_service.filter_by_group(group.id)

            for user in users:
                await poll_user(user.telegram_id, POLL_MESSAGE, reply_markup=load_attendance_kb(schedule))
