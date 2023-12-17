from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import UpdateAttendanceCallbackData
from src.dto.models import Student
from src.enums import VisitStatus
from src.kernel import Router
from src.middlewares.check_in_middleware import CheckInMiddleware
from src.resources import (
    ALL_MESSAGE,
    NONE_MESSAGE,
    attendance_buttons,
    inline_void_button,
)
from src.services import AttendanceService

__all__ = ["update_attendance_router"]


update_attendance_router = Router(must_be_registered=True)
update_attendance_router.callback_query.middleware(CheckInMiddleware())


@update_attendance_router.callback_query(UpdateAttendanceCallbackData.filter())
@logger.catch
async def update_attendance(
    callback: CallbackQuery,
    callback_data: UpdateAttendanceCallbackData,
    student: Student,
    attendance_service: AttendanceService,
):
    if callback.message is None:
        return

    if callback_data.all is not None and callback_data.all:
        await attendance_service.update_visit_status_all(student.telegram_id, VisitStatus.VISIT)
        await callback.message.edit_text(ALL_MESSAGE, reply_markup=inline_void_button())
        return

    if callback_data.all is not None and not callback_data.all:
        await attendance_service.update_visit_status_all(student.telegram_id, VisitStatus.NOT_VISIT)
        await callback.message.edit_text(NONE_MESSAGE, reply_markup=inline_void_button())
        return

    if callback_data.all is None or callback_data.lesson_id is None:
        raise TypeError("Incorrect buttons usage")

    await attendance_service.update_visit_status_for_lesson(
        student.telegram_id, callback_data.lesson_id, VisitStatus.VISIT
    )
    attendances = await attendance_service.filter_by_student_id(student.telegram_id)

    choosen_lesson = next(
        filter(lambda attendance: attendance.lesson.id == callback_data.lesson_id, attendances)
    ).lesson
    non_visit_lessons = [attendance.lesson for attendance in attendances if attendance.status != VisitStatus.VISIT]

    if non_visit_lessons:
        keyboard = attendance_buttons(non_visit_lessons)
        text = f"Вы посетите пару {choosen_lesson.name}, которая начнётся в {choosen_lesson.str_start_time}"
    else:
        keyboard = inline_void_button()
        text = ALL_MESSAGE

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
    )
