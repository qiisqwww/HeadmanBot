from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.resources import main_menu
from src.bot.headman_panel.callback_data import ShowAttendanceCallbackData
from src.bot.headman_panel.resources.inline_buttons import choose_lesson_buttons
from src.bot.headman_panel.resources.templates import (
    CHOOSE_PAIR_TEMPLATE,
    NO_LESSONS_TODAY_TEMPLATE,
    WHICH_PAIR_TEMPLATE,
)
from src.modules.attendance.application.queries import GetTodayScheduleQuery
from src.modules.student_management.domain import Role, Student

__all__ = [
    "include_get_attendance_router",
]


get_attendance_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


def include_get_attendance_router(root_router: RootRouter) -> None:
    root_router.include_router(get_attendance_router)


@get_attendance_router.callback_query(ShowAttendanceCallbackData.filter())
async def get_attendance_callback(
    callback: CallbackQuery,
    student: Student,
    get_today_schedule_query: GetTodayScheduleQuery,
    timezone: str,
) -> None:
    if callback.message is None:
        return

    schedule = await get_today_schedule_query.execute(student.group_id)

    if not schedule:
        await callback.message.answer(NO_LESSONS_TODAY_TEMPLATE)
        await callback.answer(None)
        return

    await callback.message.answer(
        CHOOSE_PAIR_TEMPLATE,
        reply_markup=main_menu(student.role),
    )
    await callback.message.answer(
        WHICH_PAIR_TEMPLATE,
        reply_markup=choose_lesson_buttons(schedule, timezone),
    )
    await callback.answer(None)
