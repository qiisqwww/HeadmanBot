from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.dto.callback_data import (
    AccessCallbackData,
    AskNewFullnameValidityCallbackData,
    AskUpdatedFieldValidityCallbackData,
    ChooseRoleCallbackData,
    GetBackToProfileCallbackData,
    ProfileUpdateCallbackData,
    ProfileUpdateChoiceCallbackData,
    UniversityCallbackData,
    UpdateAttendanceCallbackData,
)
from src.dto.models import Lesson, StudentId, University
from src.enums import ProfileField, Role

)
from src.dto.callback_data.ask_fullname_validity_callback_data import (
    AskFullnameValidityCallbackData,
)
from src.dto.models import StudentId, University
from src.enums import Role

__all__ = [
    "university_list_buttons",
    "accept_or_deny_buttons",
    "role_buttons",
    "ask_fullname_validity_buttons",
    "profile_buttons",
    "profile_update_choice_buttons",
    "is_field_correct_buttons",
    "get_back_button"
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


def ask_fullname_validity_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Да", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=True))
    builder.button(text="Нет", callback_data=AskNewFullnameValidityCallbackData(is_fullname_correct=False))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def profile_update_choice_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Редактировать имя",
        callback_data=ProfileUpdateChoiceCallbackData(updating_data=ProfileField.name)
    )
    builder.button(
        text="Редактировать фамилию",
        callback_data=ProfileUpdateChoiceCallbackData(updating_data=ProfileField.surname)
    )
    builder.button(
        text="Вернуться назад",
        callback_data=GetBackToProfileCallbackData()
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Вернуться назад",
        callback_data=GetBackToProfileCallbackData()
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def profile_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Редактировать профиль",
        callback_data=ProfileUpdateCallbackData()
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def is_field_correct_buttons(field: ProfileField) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=AskUpdatedFieldValidityCallbackData(is_field_correct=True, field_type=field)
    )
    builder.button(
        text="Нет",
        callback_data=AskUpdatedFieldValidityCallbackData(is_field_correct=False, field_type=field)
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
