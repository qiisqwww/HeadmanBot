from asyncio import TaskGroup
from typing import final

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from asyncpg import Pool
from loguru import logger

from src.modules.common.application.jobs import AsyncJob
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.attendance.infrastructure.persistence import AttendanceRepositoryImpl
from src.modules.edu_info.application.queries import GetAllGroupsQuery
from src.modules.edu_info.domain import Group
from src.modules.edu_info.infrastructure.persistence import GroupRepositoryImpl
from src.modules.student_management.application.queries import (
    GetStudentsInfoFromGroupQuery,
)
from src.modules.student_management.infrastructure.persistance import (
    StudentInfoRepositoryImpl,
)

from ..resources.inline_buttons import attendance_buttons
from ..resources.templates import POLL_TEMPLATE

__all__ = [
    "SendingJob",
]


@final
class SendingJob(AsyncJob):
    """Send everyone message which allow user to choose lessons which will be visited."""

    _bot: Bot
    _pool: Pool

    def __init__(self, bot: Bot, pool: Pool, debug: bool = False) -> None:
        self._bot = bot
        self._pool = pool

        if not debug:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 7,
                "minute": 00,
                "day_of_week": "mon-sat",
            }

    async def __call__(self) -> None:
        async with self._pool.acquire() as con:
            group_repository = GroupRepositoryImpl(con)
            get_all_groups_query = GetAllGroupsQuery(group_repository)

            groups = await get_all_groups_query.execute()

        async with TaskGroup() as tg:
            for group in groups:
                tg.create_task(self._send_to_group(group))

    async def _send_to_group(self, group: Group) -> None:
        async with self._pool.acquire() as con:
            attendance_repository = AttendanceRepositoryImpl(con)
            get_student_attedance_query = GetStudentAttendanceQuery(attendance_repository)

            student_info_repository = StudentInfoRepositoryImpl(con)
            get_students_info_from_group_query = GetStudentsInfoFromGroupQuery(student_info_repository)

            students_info = await get_students_info_from_group_query.execute(group.id)

            for student_info in students_info:
                attendances = await get_student_attedance_query.execute(student_info.id)

                try:
                    await self._bot.send_message(
                        student_info.telegram_id,
                        POLL_TEMPLATE,
                        reply_markup=attendance_buttons(student_info.is_checked_in_today, attendances),
                    )
                except TelegramForbiddenError as e:
                    logger.error(
                        f"Failed to send message to user {student_info.surname} {student_info.surname} "
                        f"id={student_info.telegram_id}"
                    )
                    logger.error(e)
