from datetime import date
from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.commands.get_attendance.domain.models import Lesson
from src.commands.get_attendance.presentation.handlers.callback_data import (
    ChooseLessonCallbackData,
    UpdateAttendanceCallbackData,
)

__all__ = [
    "attendance_buttons",
    "choose_lesson_buttons",
]


def attendance_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Буду на всех",
        callback_data=UpdateAttendanceCallbackData(all=True, day_of_poll=date.today()),
    )
    builder.button(
        text="Меня сегодня не будет",
        callback_data=UpdateAttendanceCallbackData(all=False, day_of_poll=date.today()),
    )

    for lesson in lessons:
        builder.button(
            text=f"Буду на {lesson.start_time.strftime('%H:%M')} {lesson.name}",
            callback_data=UpdateAttendanceCallbackData(lesson_id=lesson.id, day_of_poll=date.today()),
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
