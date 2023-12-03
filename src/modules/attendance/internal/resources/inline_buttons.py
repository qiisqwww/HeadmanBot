from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.modules.attendance.internal.dto import LessonDTO

__all__ = [
    "attendance_buttons",
    "choose_lesson_buttons",
]


def attendance_buttons(lessons: Iterable[LessonDTO]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [
        InlineKeyboardButton(text="Буду на всех", callback_data="attendance_all"),
        InlineKeyboardButton(text="Меня сегодня не будет", callback_data="attendance_none"),
    ]

    for lesson in lessons:
        buttons.append(
            InlineKeyboardButton(
                text=f"Буду на {lesson.start_time.strftime('%H:%M')} {lesson.name}",
                callback_data=f"attendance_{lesson.id}",
            )
        )

    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def choose_lesson_buttons(lessons: Iterable[LessonDTO]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    buttons = []

    for idx, lesson in enumerate(lessons):
        buttons.append(
            InlineKeyboardButton(
                text=f"({idx + 1}) {lesson.name} {lesson.start_time.strftime('%H:%M')}",
                callback_data=str(lesson.id),
            )
        )

    builder.add(*buttons)
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
