from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.common.resources import main_menu
from src.modules.attendance.application.queries import GetTodayScheduleQuery
from src.modules.student_management.domain import Student

from .templates import (
    NO_LESSONS_TODAY_TEMPLATE,
    schedule_list_template,
)

__all__ = [
    "include_get_schedule_command",
]


get_schedule_command_router = Router(
    must_be_registered=True,
)


def include_get_schedule_command(root_router: RootRouter) -> None:
    root_router.include_router(get_schedule_command_router)


@get_schedule_command_router.message(CommandFilter(TelegramCommand.SHOW_SCHEDULE))
async def get_attendance_command(
    message: Message,
    student: Student,
    timezone: str,
    get_today_schedule_query: GetTodayScheduleQuery,
) -> None:
    schedule = await get_today_schedule_query.execute(student.group_id)

    if not schedule:
        await message.answer(NO_LESSONS_TODAY_TEMPLATE)
        return

    await message.answer(schedule_list_template(schedule, timezone), reply_markup=main_menu(student.role))
