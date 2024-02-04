from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder

from src.bot.profile.callback_data import (
    ProfileUpdateChoiceCallbackData,
    GetBackToProfileCallbackData,
    AskUpdatedFieldValidityCallbackData,
    ProfileUpdateCallbackData
)
from src.modules.student_management.domain.enums import ProfileField

__all__ = [
    "profile_update_choice_buttons",
    "profile_buttons",
    "get_back_button",
    "is_field_correct_buttons"
]


def profile_update_choice_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Редактировать имя",
        callback_data=ProfileUpdateChoiceCallbackData(updating_data=ProfileField.NAME),
    )
    builder.button(
        text="Редактировать фамилию",
        callback_data=ProfileUpdateChoiceCallbackData(updating_data=ProfileField.SURNAME),
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


def is_field_correct_buttons(field: ProfileField) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=AskUpdatedFieldValidityCallbackData(is_field_correct=True, field_type=field),
    )
    builder.button(
        text="Нет",
        callback_data=AskUpdatedFieldValidityCallbackData(is_field_correct=False, field_type=field),
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

