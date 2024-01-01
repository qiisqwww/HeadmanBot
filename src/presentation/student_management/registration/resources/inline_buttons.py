from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.domain.edu_info import University
from src.domain.student_management import Role, StudentId

from ..callback_data import (
    AccessCallbackData,
    ChooseRoleCallbackData,
    UniversityCallbackData,
)

__all__ = [
    "university_list_buttons",
    "accept_or_deny_buttons",
    "role_buttons",
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
