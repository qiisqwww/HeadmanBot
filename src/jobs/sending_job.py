import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg.pool import PoolConnectionProxy
from loguru import logger

from src.resources.inline_buttons import load_attendance_buttons
from src.config import DEBUG
from src.database import get_pool
from src.dto.group import Group
from src.resources.messages import POLL_MESSAGE
from src.services import GroupService, LessonService, StudentService

__all__ = [
    "SendingJob",
]


class SendingJob:
    """Send everyone message which allow user to choose lessons which will be visited."""

    _scheduler: AsyncIOScheduler

    def __init__(self, bot: Bot):
        self._scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

        if DEBUG:
            self._scheduler.add_job(
                self._send,
                args=(bot,),
            )
        else:
            self._scheduler.add_job(
                self._send,
                "cron",
                day_of_week="mon-sat",
                hour=7,
                minute=00,
                args=(bot,),
            )

    def start(self):
        self._scheduler.start()

    @logger.catch
    async def _send_to_group(self, bot: Bot, con: PoolConnectionProxy, group: Group) -> None:
        lesson_service = LessonService(con)
        student_service = StudentService(con)

        lessons = await lesson_service.filter_by_group(group)

        if not lessons:
            return

        users = await student_service.filter_by_group(group)

        for user in users:
            try:
                await bot.send_message(user.telegram_id, POLL_MESSAGE, reply_markup=load_attendance_buttons(lessons))
            except TelegramForbiddenError as e:
                logger.error(f"Failed to send message to user {user.surname} {user.surname} id={user.telegram_id}")
                logger.error(e)

    @logger.catch
    async def _send(self, bot: Bot) -> None:
        logger.info("Sending job started.")

        if DEBUG:
            await asyncio.sleep(5)

        pool = await get_pool()
        async with pool.acquire() as con:
            group_service = GroupService(con)

            groups = await group_service.all()

            for group in groups:
                await self._send_to_group(bot, con, group)

        logger.info("Sending job finished.")
