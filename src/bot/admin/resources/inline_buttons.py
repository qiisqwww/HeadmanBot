from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.admin.callback_data import (
    GroupsListCallbackData,
    MakeNewAdminCallbackData,
    UsersCountCallbackData,
    DeleteUserCallbackData,
    DeleteByTGIDCallbackData,
    DeleteByNameAndGroupCallbackData
)

__all__ = [
    "admin_panel_buttons",
    "delete_user_choice_buttons"
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
        text="Удалить пользоватля",
        callback_data=DeleteUserCallbackData()
    )
    builder.button(
        text="Назначить администратора (в разработке)",
        callback_data=MakeNewAdminCallbackData()
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def delete_user_choice_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Удалить через telegram ID",
        callback_data=DeleteByTGIDCallbackData()
    )
    builder.button(
        text="Удалить через Фамилию, Имя и название группы",
        callback_data=DeleteByNameAndGroupCallbackData()
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
