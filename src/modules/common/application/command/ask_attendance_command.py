import asyncio
from typing import final

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from injector import inject
from loguru import logger

from src.bot.poll_attendance.resources.inline_buttons import update_attendance_buttons
from src.bot.poll_attendance.resources.templates import (
    POLL_TEMPLATE,
    student_was_not_polled_warning_template,
)
from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.common.application import WithArgsUseCase
from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.common.infrastructure.facade import FacadeImpl
from src.modules.edu_info.application.repositories import GroupRepository
from src.modules.edu_info.application.repositories.university_repository import UniversityRepository
from src.modules.student_management.application.repositories.student_info_repository import StudentInfoRepository
from src.modules.student_management.application.repositories.student_repository import StudentRepository
from src.modules.student_management.domain import StudentInfo
from src.modules.student_management.domain.enums.role import Role

__all__ = [
    "AskAttendanceCommand",
]


@final
class AskStudentAttendanceCommand(WithArgsUseCase):
    _attendance_repository: AttendanceRepository
    _student_repository: StudentRepository

    _bot: Bot
    _notifier: BotNotifier

    @inject
    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        student_repository: StudentRepository,
        notifier: BotNotifier,
        bot: Bot,
    ) -> None:
        self._attendance_repository = attendance_repository
        self._student_repository = student_repository

        self._bot = bot
        self._notifier = notifier

    async def execute(
        self,
        student_info: StudentInfo,
        timezone: str,
        headman_telegram_id: int,
    ) -> None:
        try:
            attendances = await self._attendance_repository.filter_by_student_id(student_info.id)

            if len(attendances) == 0:
                return

            try:
                await self._bot.send_message(
                    student_info.telegram_id,
                    POLL_TEMPLATE,
                    reply_markup=update_attendance_buttons(
                        student_info.attendance_noted,
                        attendances,
                        timezone,
                    ),
                )

            except TelegramForbiddenError:
                await self._bot.send_message(
                    headman_telegram_id,
                    student_was_not_polled_warning_template(student_info),
                )

                await self._student_repository.delete_by_telegram_id(student_info.telegram_id)

        except Exception as e:
            logger.info(student_info)
            try:
                await self._student_repository.delete_by_telegram_id(student_info.telegram_id)
            except:
                logger.info("User already been deleted")

            await self._notifier.notify_about_job_exception(
                e,
                self.__class__.__name__,
            )


@final
class AskAttendanceCommand(FacadeImpl):
    _group_repository: GroupRepository
    _university_repository: UniversityRepository
    _student_info_repository: StudentInfoRepository
    _student_repository: StudentRepository

    @inject
    def __init__(
        self,
        group_repository: GroupRepository,
        university_repository: UniversityRepository,
        student_repository: StudentRepository,
        student_info_repository: StudentInfoRepository,
    ) -> None:
        self._group_repository = group_repository
        self._university_repository = university_repository
        self._student_info_repository = student_info_repository
        self._student_repository = student_repository

    async def execute(self) -> None:
        groups = await self._group_repository.all()

        for group in groups:
            group_timezone = await self._university_repository.fetch_university_timezone_by_group_id(group.id)
            students = await self._student_info_repository.filter_by_group_id(group.id)
            headman = await self._student_repository.find_by_group_id_and_role(group.id, Role.HEADMAN)
            headman_telegram_id = headman.telegram_id

            tasks = [
                self.run_command_isolated(AskStudentAttendanceCommand, student, group_timezone, headman_telegram_id)
                for student in students
            ]
            asyncio.gather(*tasks)
