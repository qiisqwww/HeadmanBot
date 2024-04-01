from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable

__all__ = [
    "ChooseLessonCallbackData",
]


class ChooseLessonCallbackData(
    Expirerable,
    CallbackData,
    prefix="choose_lesson_for_headman",
):
    lesson_id: int
