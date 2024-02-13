from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.common.convert_time import convert_time_from_utc
from src.bot.common.trim_inline_text import trim_inline_text
from src.bot.show_group_attendance.callback_data import ChooseLessonCallbackData
from src.modules.attendance.domain import Lesson

__all__ = [
    "choose_lesson_buttons",
]


def choose_lesson_buttons(
    lessons: Iterable[Lesson],
    student_timezone: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for lesson in lessons:
        start_time = convert_time_from_utc(lesson.start_time, student_timezone)
        button_text = trim_inline_text(f"{start_time:%H:%M} {lesson.name}")
        builder.button(
            text=button_text,
            callback_data=ChooseLessonCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
