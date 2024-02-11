from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.show_group_attendance.callback_data import ChooseLessonCallbackData
from src.bot.show_group_attendance.resources import attendance_for_headmen_template, choose_lesson_buttons
from src.modules.attendance.application.queries import (
    GetLessonAttendanceForGroupQuery,
    GetTodayScheduleQuery,
)
from src.modules.student_management.domain import Role, Student

__all__ = [
    "include_choose_lesson_callback_router",
]


choose_lesson_callback_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


def include_choose_lesson_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_lesson_callback_router)


@choose_lesson_callback_router.callback_query(ChooseLessonCallbackData.filter())
async def attendance_send_callback(
    callback: CallbackQuery,
    callback_data: ChooseLessonCallbackData,
    student: Student,
    get_today_schedule_query: GetTodayScheduleQuery,
    get_visit_status_for_group_students_query: GetLessonAttendanceForGroupQuery,
    timezone: str,
) -> None:
    if callback.message is None:
        return

    schedule = await get_today_schedule_query.execute(student.group_id)
    choosen_lesson = next((lesson for lesson in schedule if lesson.id == callback_data.lesson_id), None)

    if choosen_lesson is None:
        await callback.message.edit_text("Сегодня пар нет.")
    group_attendance = await get_visit_status_for_group_students_query.execute(student.group_id, choosen_lesson.id)

    new_message = attendance_for_headmen_template(choosen_lesson, group_attendance, timezone)

    if new_message == callback.message.html_text:
        await callback.answer(None)
    else:
        await callback.message.edit_text(new_message, reply_markup=choose_lesson_buttons(schedule, timezone))
