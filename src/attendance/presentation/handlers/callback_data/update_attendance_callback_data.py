from datetime import date

from aiogram.filters.callback_data import CallbackData

from src.commands.get_attendance.domain.models import LessonId

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(CallbackData, prefix="update_attendace_prefix"):  # type: ignore
    all: bool | None = None
    lesson_id: LessonId | None = None
    day_of_poll: date
