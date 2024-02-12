from asyncio import TaskGroup
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import final

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from injector import Injector
from loguru import logger

from src.bot.poll_attendance.resources import POLL_TEMPLATE, update_attendance_buttons
from src.bot.poll_attendance.resources.templates import student_was_not_polled_warning_template
from src.modules.attendance.application.queries import GetStudentAttendanceQuery
from src.modules.attendance.domain import StudentInfo
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.scheduling import AsyncJob
from src.modules.edu_info.application.queries import FetchUniTimezonByGroupIdQuery, GetAllGroupsQuery
from src.modules.edu_info.domain import Group
from src.modules.student_management.application.queries import (
    FindGroupHeadmanQuery,
    GetStudentsInfoFromGroupQuery,
)

__all__ = [
    "SendingJob",
]


@final
class SendingJob(AsyncJob):
    """Send everyone message which allow user to choose lessons which will be visited."""

    _bot: Bot
    _build_container: Callable[[], AbstractAsyncContextManager[Injector]]

    def __init__(self, bot: Bot, build_container: Callable[[], AbstractAsyncContextManager[Injector]]) -> None:
        self._bot = bot
        self._build_container = build_container

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 7,
                "minute": 00,
                "day_of_week": "mon-sat",
            }

    @logger.catch
    async def __call__(self) -> None:
        logger.info("Start sending job.")
        async with self._build_container() as container:
            get_all_groups_query = container.get(GetAllGroupsQuery)
            groups = await get_all_groups_query.execute()
            get_students_info_from_group_query = container.get(GetStudentsInfoFromGroupQuery)

            fetch_group_timezone = container.get(FetchUniTimezonByGroupIdQuery)
            find_group_headman_query = container.get(FindGroupHeadmanQuery)

            for group in groups:
                timezone = await fetch_group_timezone.execute(group.id)
                await self._send_to_group(
                    group,
                    get_students_info_from_group_query,
                    find_group_headman_query,
                    timezone,
                )
        logger.info("Stop sending job.")

    @logger.catch
    async def _send_to_group(
        self,
        group: Group,
        get_students_info_from_group_query: GetStudentsInfoFromGroupQuery,
        find_group_headman_query: FindGroupHeadmanQuery,
        timezone: str,
    ) -> None:
        students_info = await get_students_info_from_group_query.execute(group.id)
        group_headman = await find_group_headman_query.execute(group.id)

        async with TaskGroup() as tg:
            for student_info in students_info:
                tg.create_task(self._send_to_student(student_info, group_headman.id, timezone))


    @logger.catch
    async def _send_to_student(self, student_info: StudentInfo, headman_telegram_id: int, timezone: str) -> None:
        async with self._build_container() as container:
            get_student_attedance_query = container.get(GetStudentAttendanceQuery)
            attendances = await get_student_attedance_query.execute(student_info.id)
            attendances.sort()

            try:
                await self._bot.send_message(
                    student_info.telegram_id,
                    POLL_TEMPLATE,
                    reply_markup=update_attendance_buttons(student_info.attendance_noted, attendances, timezone),
                )
            except TelegramForbiddenError:
                try:
                    await self._bot.send_message(
                        headman_telegram_id,
                        student_was_not_polled_warning_template(student_info),
                    )
                except Exception as e:
                    logger.exception(e)

            except Exception as e:
                logger.exception(e)
