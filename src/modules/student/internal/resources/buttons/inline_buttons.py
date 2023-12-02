from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.kernel.role import Role
from src.modules.student.internal.controllers.unregistred.callback_data import (
    AccessCallbackData,
    RoleCallbackData,
    UniversityCallbackData,
)
from src.modules.university.api.dto import UniversityDTO

__all__ = [
    "university_list_buttons",
    "accept_or_deny_buttons",
    "role_buttons",
    "inline_void_button",
]


def inline_void_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup(resize_keyboard=True)


def university_list_buttons(universities: Iterable[UniversityDTO]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uni in universities:
        builder.button(text=uni.name, callback_data=UniversityCallbackData(university_alias=uni.alias))

    return builder.as_markup(resize_keyboard=True)


def role_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Я студент", callback_data=RoleCallbackData(role=Role.STUDENT))
    builder.button(text="Я староста", callback_data=RoleCallbackData(role=Role.HEADMAN))

    return builder.as_markup(resize_keyboard=True)


def accept_or_deny_buttons(student_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Одобрить", callback_data=AccessCallbackData(student_id=student_id, accepted=True))
    builder.button(text="Отказать", callback_data=AccessCallbackData(student_id=student_id, accepted=False))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
