from asyncio import TaskGroup
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, suppress
from typing import final

from aiogram import Bot
from aiogram.types import BufferedInputFile
from injector import Injector
from loguru import logger

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
    "PollByRoleJob",
]


@final
class PollByRoleJob(AsyncJob):
    """Send to students a notify message basing on their role."""

    _bot: Bot
    _build_container: Callable[[], AbstractAsyncContextManager[Injector]]

    def __init__(
        self,
        bot: Bot,
        build_container: Callable[[], AbstractAsyncContextManager[Injector]],
    ) -> None:
        self._bot = bot
        self._build_container = build_container

        if not DEBUG:
            self._trigger = "cron"
            self._trigger_args = {
                "hour": 8,
                "minute": 15,
                "day_of_week": "mon-sat",
            }

    async def __call__(self) -> None:
        async with self._build_container() as container:
            get_all_groups_query = container.get(GetAllGroupsQuery)
            groups = await get_all_groups_query.execute()
            get_students_info_from_group_query = container.get(
                GetStudentsInfoFromGroupQuery,
            )
            get_student_role_by_telegram_id_query = container.get(
                GetStudentRoleByTelegramIDQuery,
            )

            with open("poll_by_role.html", "r+") as update_info_file, open("ShowInfoImg.png", "rb") as photo:
                photo_content = photo.read()
                update_info = update_info_file.read()
                if len(update_info) == 0:
                    return

                for group in groups:
                    await self._send_to_group(
                        group,
                        get_students_info_from_group_query,
                        get_student_role_by_telegram_id_query,
                        update_info,
                        photo_content,
                    )

                update_info_file.truncate(0)
                update_info_file.flush()
        logger.info("Finish poll by role job.")

    async def _send_to_group(
        self,
        group: Group,
        get_students_info_from_group_query: GetStudentsInfoFromGroupQuery,
        get_student_role_by_telegram_id_query: GetStudentRoleByTelegramIDQuery,
        update_info: str,
        photo: bytes,
    ) -> None:
        students_info = await get_students_info_from_group_query.execute(group.id)

        async with TaskGroup() as tg:
            for student_info in students_info:
                student_role: Role = (
                    await get_student_role_by_telegram_id_query.execute(
                        student_info.telegram_id,
                    )
                )
                tg.create_task(
                    self._send_to_student(student_info, update_info, student_role, photo),
                )

    async def _send_to_student(
        self,
        student_info: StudentInfo,
        update_info: str,
        student_role: Role,
        photo: bytes,
    ) -> None:
        student_text, headman_text = update_info.split("aboba")

        with suppress(Exception):
            # Trust me. I am not going to apologize for this sheet code **BUT IT MUST BE REFACTORED**
            # if student_role == Role.STUDENT:
            #    await self._bot.send_message(
            #        student_info.telegram_id,
            #        student_text,
            #    )

            if student_role == Role.HEADMAN:
                await self._bot.send_photo(
                    student_info.telegram_id,
                    photo=BufferedInputFile(photo, "img.png"),
                    caption=headman_text,
                )
