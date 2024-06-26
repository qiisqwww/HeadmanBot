from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ChooseLessonCallbackData",
]


class ChooseLessonCallbackData(
    Expireable,
    CallbackData,
    prefix="choose_lesson_for_headman",
):
    lesson_id: int
