from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.change_group.callback_data import (
    ChangeGroupCallbackData,
    CancelActionCallbackData,
    QuitGroupCallbackData,
    GetBackCallbackData
)

__all__ = [
    "change_group_buttons",
    "get_back_button"
]


def change_group_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Изменить группу", callback_data=ChangeGroupCallbackData())
    builder.button(text="Выйти из группы", callback_data=QuitGroupCallbackData())
    builder.button(text="Отмена", callback_data=CancelActionCallbackData())

    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_back_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Вернуться назад", callback_data=GetBackCallbackData())
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
