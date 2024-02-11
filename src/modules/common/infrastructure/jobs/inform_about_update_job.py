from asyncio import TaskGroup
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, suppress
from typing import final

from aiogram import Bot
from injector import Injector

from src.bot.common.resources.main_menu import main_menu
from src.modules.common.infrastructure.config import DEBUG
from src.modules.common.infrastructure.scheduling import AsyncJob
from src.modules.edu_info.application.queries import GetAllGroupsQuery
from src.modules.edu_info.domain import Group
from src.modules.student_management.application.queries import (
    GetStudentRoleByTelegramIDQuery,
    GetStudentsInfoFromGroupQuery,
)
from src.modules.student_management.domain import StudentInfo
from src.modules.student_management.domain.enums import Role

__all__ = [
    "InformAboutUpdateJob",
]


@final
class InformAboutUpdateJob(AsyncJob):
    """Send everyone message with information about previous update."""

    _bot: Bot
    _build_container: Callable[[], AbstractAsyncContextManager[Injector]]

    def __init__(self, bot: Bot, build_container: Callable[[], AbstractAsyncContextManager[Injector]]) -> None:
        self._bot = bot
        self._build_container = build_container

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 20,
                "minute": 00,
                "day_of_week": "mon-sat",
            }

        if DEBUG:
            self._trigger = "interval"
            self._trigger_args = {
                "seconds": 10,
            }

    async def __call__(self) -> None:
        async with self._build_container() as container:
            get_all_groups_query = container.get(GetAllGroupsQuery)
            groups = await get_all_groups_query.execute()
            get_students_info_from_group_query = container.get(GetStudentsInfoFromGroupQuery)
            get_student_role_by_telegram_id_query = container.get(GetStudentRoleByTelegramIDQuery)

            with open("update_info.html", "r+") as update_info_file:
                update_info = update_info_file.read()
                if len(update_info) == 0:
                    return

                for group in groups:
                    await self._send_to_group(
                        group,
                        get_students_info_from_group_query,
                        get_student_role_by_telegram_id_query,
                        update_info,
                    )

                update_info_file.truncate(0)
                update_info_file.flush()

    async def _send_to_group(
        self,
        group: Group,
        get_students_info_from_group_query: GetStudentsInfoFromGroupQuery,
        get_student_role_by_telegram_id_query: GetStudentRoleByTelegramIDQuery,
        update_info: str,
    ) -> None:
        students_info = await get_students_info_from_group_query.execute(group.id)

        async with TaskGroup() as tg:
            for student_info in students_info:
                student_role: Role = await get_student_role_by_telegram_id_query.execute(student_info.telegram_id)
                tg.create_task(self._send_to_student(student_info, update_info, student_role))

    async def _send_to_student(self, student_info: StudentInfo, update_info: str, student_role: Role) -> None:
        with suppress(Exception):
            await self._bot.send_message(
                student_info.telegram_id,
                update_info,
                reply_markup=main_menu(student_role),
            )
