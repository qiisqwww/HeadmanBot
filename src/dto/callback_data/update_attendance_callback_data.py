from aiogram.filters.callback_data import CallbackData

from src.dto.models import LessonId

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(CallbackData, prefix="update_attendace"):  # type: ignore
    all: bool | None
    lesson_id: LessonId | None
