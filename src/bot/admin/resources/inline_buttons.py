from aiogram.filters.callback_data import CallbackData
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.admin.callback_data import (
    GroupsListCallbackData,
    MakeNewAdminCallbackData,
    UsersCountCallbackData
)

__all__ = [
    "admin_panel_buttons"
]


def admin_panel_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Узнать количество пользователей",
        callback_data=UsersCountCallbackData(),
    )
    builder.button(
        text="Получить информацию по всем группам",
        callback_data=GroupsListCallbackData()
    )
    builder.button(
        text="Назначить администратора (в разработке)"
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
