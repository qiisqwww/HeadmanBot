from aiogram.filters.callback_data import CallbackData

from src.dto.models import LessonId

__all__ = [
    "ChooseLessonCallbackData",
]


class ChooseLessonCallbackData(CallbackData, prefix="choose_lesson_for_headman"):  # type: ignore
    lesson_id: LessonId
