import asyncio
from typing import final

from aiogram.exceptions import TelegramForbiddenError
from loguru import logger

from src.bot.poll_attendance.resources.inline_buttons import update_attendance_buttons
from src.bot.poll_attendance.resources.templates import (
    POLL_TEMPLATE,
    student_was_not_polled_warning_template,
)
from src.common.bot_notifier import BotNotifier
from src.common.database import DbContext
from src.common.facade import Facade
from src.common.use_case import WithArgsUseCase
from src.dto.entities import Student
from src.dto.enums import Role
from src.repositories import AttendanceRepository, GroupRepository, UniversityRepository, StudentRepository

__all__ = [
    "AskAttendanceCommand",
]


@final
class AskStudentAttendanceCommand(WithArgsUseCase):
    _attendance_repository: AttendanceRepository
    _student_repository: StudentRepository
    _notifier: BotNotifier

    def __init__(self, con: DbContext) -> None:
        self._attendance_repository = AttendanceRepository(con)
        self._student_repository = StudentRepository(con)
        self._notifier = BotNotifier()

    async def execute(
            self,
            student: Student,
            timezone: str,
            headman_telegram_id: int,
    ) -> None:
        try:
            attendances = await self._attendance_repository.filter_by_student_id(student.id)

            if not attendances:
                return

            try:
                await self._bot.send_message(
                    student.telegram_id,
                    POLL_TEMPLATE,
                    reply_markup=update_attendance_buttons(
                        student.attendance_noted,
                        attendances,
                        timezone,
                    ),
                )

            except TelegramForbiddenError:
                await self._notifier._bot.send_message(
                    headman_telegram_id,
                    student_was_not_polled_warning_template(student),
                )

                await self._student_repository.delete_by_telegram_id(student.telegram_id)

        except Exception as e:
            try:
                await self._student_repository.delete_by_telegram_id(student.telegram_id)
            except:
                logger.info("User already been deleted")

            await self._notifier.notify_about_job_exception(
                e,
                self.__class__.__name__,
            )


@final
class AskAttendanceCommand(Facade):
    _group_repository: GroupRepository
    _university_repository: UniversityRepository
    _student_repository: StudentRepository

    def __init__(self, pool) -> None:
        super().__init__(pool)
        con = DbContext(pool=pool)
        con.open()

        self._group_repository = GroupRepository(con)
        self._university_repository = UniversityRepository(con)
        self._student_repository = StudentRepository(con)

    async def execute(self) -> None:
        groups = await self._group_repository.all()

        for group in groups:
            group_timezone = await self._university_repository.fetch_university_timezone_by_group_id(group.id)
            students = await self._student_repository.filter_by_group_id(group.id)
            headman = await self._student_repository.find_by_group_id_and_role(group.id, Role.HEADMAN)

            tasks = [
                self.run_command_isolated(
                    AskStudentAttendanceCommand, student, group_timezone, headman.telegram_id
                )
                for student in students
            ]
            await asyncio.gather(*tasks)
