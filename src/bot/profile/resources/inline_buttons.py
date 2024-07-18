from collections.abc import Iterable

from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.profile.callback_data import (
    AskUpdatedBirthdateValidityCallbackData,
    AskUpdatedNameValidityCallbackData,
    AskUpdatedSurnameValidityCallbackData,
    GetBackToProfileCallbackData,
    ProfileUpdateBirthdateCallbackData,
    ProfileUpdateCallbackData,
    ProfileUpdateNameCallbackData,
    ProfileUpdateSurnameCallbackData,
    LeaveGroupCallbackData,
    EnterGroupCallbackData,
    SureToLeaveGroupCallbackData,
    ChooseNewRoleCallbackData,
    ChooseUniCallbackData,
    AcceptStudentEnterGroupCallbackData
)
from src.bot.profile.profile_field import ProfileField
from src.modules.student_management.domain import Role, UniversityInfo

__all__ = [
    "profile_update_choice_buttons",
    "profile_buttons",
    "get_back_button",
    "is_field_correct_buttons",
    "sure_to_leave_group_buttons",
    "role_buttons",
    "university_list_buttons",
    "accept_or_deny_buttons"
]


def profile_update_choice_buttons(has_group: bool, is_headman: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Редактировать имя",
        callback_data=ProfileUpdateNameCallbackData(),
    )
    builder.button(
        text="Редактировать фамилию",
        callback_data=ProfileUpdateSurnameCallbackData(),
    )
    builder.button(
        text="Редактировать дату рождения",
        callback_data=ProfileUpdateBirthdateCallbackData(),
    )
    if not is_headman:
        if has_group:
            builder.button(
                text="Выйти из группы",
                callback_data=LeaveGroupCallbackData()
            )
        else:
            builder.button(
                text="Войти в группу",
                callback_data=EnterGroupCallbackData()
            )
    builder.button(
        text="Вернуться в профиль",
        callback_data=GetBackToProfileCallbackData()
    )
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Вернуться назад", callback_data=ProfileUpdateCallbackData())
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def profile_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Редактировать профиль", callback_data=ProfileUpdateCallbackData())

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def make_ask_validity_callback_data(field: ProfileField, is_field_correct: bool) -> CallbackData:
    match field:
        case ProfileField.FIRST_NAME:
            return AskUpdatedNameValidityCallbackData(is_field_correct=is_field_correct)
        case ProfileField.LAST_NAME:
            return AskUpdatedSurnameValidityCallbackData(is_field_correct=is_field_correct)
        case ProfileField.BIRTHDATE:
            return AskUpdatedBirthdateValidityCallbackData(is_field_correct=is_field_correct)


def is_field_correct_buttons(field: ProfileField) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=make_ask_validity_callback_data(field, True),
    )
    builder.button(
        text="Нет",
        callback_data=make_ask_validity_callback_data(field, False),
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def sure_to_leave_group_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=SureToLeaveGroupCallbackData(is_user_sure=True)
    )
    builder.button(
        text="Нет",
        callback_data=SureToLeaveGroupCallbackData(is_user_sure=False)
    )
    builder.button(
        text="Вернуться назад", callback_data=ProfileUpdateCallbackData()
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def role_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Я студент", callback_data=ChooseNewRoleCallbackData(role=Role.STUDENT),
    )
    builder.button(
        text="Я староста", callback_data=ChooseNewRoleCallbackData(role=Role.HEADMAN),
    )
    builder.button(
        text="Вернуться назад", callback_data=ProfileUpdateCallbackData()
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def university_list_buttons(
    universities: Iterable[UniversityInfo],
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uni in universities:
        builder.button(
            text=uni.name,
            callback_data=ChooseUniCallbackData(university_alias=uni.alias),
        )
    builder.button(
        text="Вернуться назад", callback_data=ProfileUpdateCallbackData()
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def accept_or_deny_buttons(student_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Одобрить",
        callback_data=AcceptStudentEnterGroupCallbackData(telegram_id=student_id, accepted=True),
    )
    builder.button(
        text="Отказать",
        callback_data=AcceptStudentEnterGroupCallbackData(telegram_id=student_id, accepted=False),
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
