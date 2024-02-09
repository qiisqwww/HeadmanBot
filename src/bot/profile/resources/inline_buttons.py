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
)
from src.bot.profile.profile_field import ProfileField

__all__ = [
    "profile_update_choice_buttons",
    "profile_buttons",
    "get_back_button",
    "is_field_correct_buttons",
]


def profile_update_choice_buttons() -> InlineKeyboardMarkup:
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
    builder.button(text="Вернуться в профиль", callback_data=GetBackToProfileCallbackData())
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Вернуться назад", callback_data=GetBackToProfileCallbackData())
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
