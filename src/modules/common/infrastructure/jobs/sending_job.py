from asyncio import TaskGroup
from collections.abc import Callable
from typing import AsyncContextManager, final

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from injector import Injector
from loguru import logger

from src.bot.modules.attendance.resources.inline_buttons import attendance_buttons
from src.bot.modules.attendance.resources.templates import POLL_TEMPLATE
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.common.infrastructure.config.config import DEBUG
from src.modules.common.infrastructure.scheduling import AsyncJob
from src.modules.edu_info.application.queries import GetAllGroupsQuery
from src.modules.edu_info.domain import Group
from src.modules.student_management.application.queries import (
    GetStudentsInfoFromGroupQuery,
)
from src.modules.student_management.domain import StudentInfo

__all__ = [
    "SendingJob",
]


@final
class SendingJob(AsyncJob):
    """Send everyone message which allow user to choose lessons which will be visited."""

    _bot: Bot
    _build_container: Callable[[], AsyncContextManager[Injector]]

    def __init__(self, bot: Bot, build_container: Callable[[], AsyncContextManager[Injector]]) -> None:
        self._bot = bot
        self._build_container = build_container

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 7,
                "minute": 00,
                "day_of_week": "mon-sat",
            }

    async def __call__(self) -> None:
        async with self._build_container() as container:
            get_all_groups_query = container.get(GetAllGroupsQuery)
            groups = await get_all_groups_query.execute()
            get_students_info_from_group_query = container.get(GetStudentsInfoFromGroupQuery)

            for group in groups:
                await self._send_to_group(group, get_students_info_from_group_query)

    async def _send_to_group(
        self, group: Group, get_students_info_from_group_query: GetStudentsInfoFromGroupQuery
    ) -> None:
        students_info = await get_students_info_from_group_query.execute(group.id)

        async with TaskGroup() as tg:
            for student_info in students_info:
                tg.create_task(self._send_to_student(student_info))

    async def _send_to_student(self, student_info: StudentInfo) -> None:
        async with self._build_container() as container:
            get_student_attedance_query = container.get(GetStudentAttendanceQuery)
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
                    f"id={student_info.telegram_id} because of\n{e}",
                )
