from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.admin.callback_data import (
    CancelActionCallbackData,
    DeleteByNameAndGroupCallbackData,
    DeleteByTGIDCallbackData,
    DeleteStudentCallbackData,
    GroupsListCallbackData,
    MakeNewAdminCallbackData,
    StudentsCountCallbackData,
)

__all__ = [
    "admin_panel_buttons",
    "delete_user_choice_buttons",
    "cancel_button",
]


def admin_panel_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Узнать количество пользователей",
        callback_data=StudentsCountCallbackData(),
    )
    builder.button(
        text="Получить информацию по всем группам",
        callback_data=GroupsListCallbackData(),
    )
    builder.button(
        text="Удалить пользователя",
        callback_data=DeleteStudentCallbackData(),
    )
    builder.button(
        text="Назначить администратора (в разработке)",
        callback_data=MakeNewAdminCallbackData(),
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def delete_user_choice_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Удалить через telegram ID",
        callback_data=DeleteByTGIDCallbackData(),
    )
    builder.button(
        text="Удалить через Фамилию, Имя и название группы",
        callback_data=DeleteByNameAndGroupCallbackData(),
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def cancel_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Отмена",
        callback_data=CancelActionCallbackData(),
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
