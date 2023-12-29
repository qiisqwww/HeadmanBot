from datetime import date
from typing import Iterable
from loguru import logger

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.dto.callback_data import (
    AccessCallbackData,
    ChooseLessonCallbackData,
    ChooseRoleCallbackData,
    UniversityCallbackData,
    UpdateAttendanceCallbackData,
    AskNewFullnameValidityCallbackData,
    AskEditedFullnameValidityCallbackData
)
from src.dto.models import Lesson, StudentId, University
from src.enums import Role

__all__ = [
    "university_list_buttons",
    "accept_or_deny_buttons",
    "role_buttons",
    "attendance_buttons",
    "choose_lesson_buttons",
    "ask_fullname_validity_buttons",
]


def university_list_buttons(universities: Iterable[University]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uni in universities:
        builder.button(text=uni.name, callback_data=UniversityCallbackData(university_alias=uni.alias))

    return builder.as_markup(resize_keyboard=True)


def role_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Я студент", callback_data=ChooseRoleCallbackData(role=Role.STUDENT))
    builder.button(text="Я староста", callback_data=ChooseRoleCallbackData(role=Role.HEADMAN))

    return builder.as_markup(resize_keyboard=True)


def accept_or_deny_buttons(student_id: StudentId) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Одобрить", callback_data=AccessCallbackData(student_id=student_id, accepted=True))
    builder.button(text="Отказать", callback_data=AccessCallbackData(student_id=student_id, accepted=False))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


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


def ask_fullname_validity_buttons(is_editing: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if is_editing:
        builder.button(text="Да", callback_data=AskEditedFullnameValidityCallbackData(is_fullname_correct=True))
        builder.button(text="Нет", callback_data=AskEditedFullnameValidityCallbackData(is_fullname_correct=False))
        builder.adjust(2)

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    builder.button(text="Да", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=True))
    builder.button(text="Нет", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=False))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
