from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.registration.callback_data import (
    AccessCallbackData,
    AskNewFullnameValidityCallbackData,
    ChooseRoleCallbackData,
    UniversityCallbackData
)
from src.modules.student_management.domain import Role, UniversityInfo

__all__ = [
    "university_list_buttons",
    "accept_or_deny_buttons",
    "role_buttons",
    "ask_fullname_validity_buttons",
]


def university_list_buttons(universities: Iterable[UniversityInfo]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uni in universities:
        builder.button(text=uni.name, callback_data=UniversityCallbackData(university_alias=uni.alias))

    return builder.as_markup(resize_keyboard=True)


def role_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Я студент", callback_data=ChooseRoleCallbackData(role=Role.STUDENT))
    builder.button(text="Я староста", callback_data=ChooseRoleCallbackData(role=Role.HEADMAN))

    return builder.as_markup(resize_keyboard=True)


def accept_or_deny_buttons(student_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Одобрить", callback_data=AccessCallbackData(telegram_id=student_id, accepted=True))
    builder.button(text="Отказать", callback_data=AccessCallbackData(telegram_id=student_id, accepted=False))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def ask_fullname_validity_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=True))
    builder.button(text="Нет", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=False))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
