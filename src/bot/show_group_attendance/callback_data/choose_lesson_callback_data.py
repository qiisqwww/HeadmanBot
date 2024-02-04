from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ChooseLessonCallbackData",
]


class ChooseLessonCallbackData(CallbackData, prefix="choose_lesson_for_headman"):  # type: ignore
    lesson_id: int
