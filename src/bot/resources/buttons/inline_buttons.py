from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.dto import Lesson
from src.handlers.callback_data import AccessCallbackFactory

__all__ = [
    "attendance_buttons",
    "choose_lesson_buttons",
    "accept_or_deny_buttons",
    "university_list_buttons",
    "role_buttons",
]


def accept_or_deny_buttons(student_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Одобрить", callback_data=AccessCallbackFactory(student_id=student_id, accepted=True))
    builder.button(text="Отказать", callback_data=AccessCallbackFactory(student_id=student_id, accepted=False))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def attendance_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
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


def choose_lesson_buttons(lessons: Iterable[Lesson]) -> InlineKeyboardMarkup:
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
