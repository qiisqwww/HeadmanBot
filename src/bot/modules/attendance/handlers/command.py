from aiogram.types import Message
from loguru import logger

from src.dto.models import Student
from src.enums import Role
from src.kernel import Router
from src.kernel.command_filter import CommandFilter, TelegramCommand
from src.resources.buttons import main_menu

from ...domain.services import ScheduleService
from ..resources.inline_buttons import choose_lesson_buttons
from ..resources.templates import (
    CHOOSE_PAIR_TEMPLATE,
    NO_LESSONS_TODAY_TEMPLATE,
    WHICH_PAIR_TEMPLATE,
)

__all__ = [
    "get_attendance_command_router",
]


get_attendance_command_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


@get_attendance_command_router.message(CommandFilter(TelegramCommand.GET_ATTENDANCE))
@logger.catch
async def get_attendance_command(message: Message, student: Student, schedule_service: ScheduleService) -> None:
    schedule = await schedule_service.get_group_schedule(student.group)

    if not schedule:
        await message.answer(NO_LESSONS_TODAY_TEMPLATE)
        return

    await message.answer(CHOOSE_PAIR_TEMPLATE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_TEMPLATE, reply_markup=choose_lesson_buttons(schedule.lessons))
