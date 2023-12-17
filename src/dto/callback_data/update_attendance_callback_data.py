from datetime import date

from aiogram.filters.callback_data import CallbackData

from src.dto.models import LessonId

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(CallbackData, prefix="update_attendace_prefix"):  # type: ignore
    all: bool | None = None
    lesson_id: LessonId | None = None
    day_of_poll: date
