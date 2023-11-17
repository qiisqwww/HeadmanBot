from typing import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.dto import Lesson

__all__ = [
    "load_attendance_buttons",
    "load_choose_lesson_buttons",
    "load_headman_kb",
]


def load_attendance_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
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


def load_choose_lesson_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
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


def load_headman_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(*[KeyboardButton(text="/getstat"), KeyboardButton(text="/faq")])

    return builder.as_markup(resize_keyboard=True)
