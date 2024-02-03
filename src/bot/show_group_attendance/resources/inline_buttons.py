from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.show_group_attendance.callback_data import ChooseLessonCallbackData
from src.modules.attendance.domain import Lesson

__all__ = [
    "choose_lesson_buttons",
]

def choose_lesson_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, lesson in enumerate(lessons):
        builder.button(
            text=f"({idx + 1}) {lesson.name} {lesson.start_time.strftime('%H:%M')}",
            callback_data=ChooseLessonCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
