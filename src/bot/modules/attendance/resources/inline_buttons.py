from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.modules.attendance.domain import Lesson

from ..callback_data import ChooseLessonCallbackData, UpdateAttendanceCallbackData

__all__ = [
    "attendance_buttons",
    "choose_lesson_buttons",
]


def attendance_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Буду на всех",
        callback_data=UpdateAttendanceCallbackData(all=True),
    )
    builder.button(
        text="Меня сегодня не будет",
        callback_data=UpdateAttendanceCallbackData(all=False),
    )

    for lesson in lessons:
        builder.button(
            text=f"Буду на {lesson.start_time.strftime('%H:%M')} {lesson.name}",
            callback_data=UpdateAttendanceCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def choose_lesson_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for idx, lesson in enumerate(lessons):
        builder.button(
            text=f"({idx + 1}) {lesson.name} {lesson.start_time.strftime('%H:%M')}",
            callback_data=ChooseLessonCallbackData(lesson_id=lesson.id),
        )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
