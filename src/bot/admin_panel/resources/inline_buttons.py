from collections.abc import Iterable

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.admin_panel.callback_data import (
    CancelActionCallbackData,
    DeleteByNameAndGroupCallbackData,
    DeleteByTGIDCallbackData,
    DeleteStudentCallbackData,
    GroupsListCallbackData,
    MakeNewAdminCallbackData,
    StudentsCountCallbackData,
    ChangeGroupCallbackData,
    ChooseUniCallbackData
)
from src.modules.student_management.domain import UniversityInfo

__all__ = [
    "admin_panel_buttons",
    "delete_user_choice_buttons",
    "cancel_button",
    "university_list_buttons"
]


def admin_panel_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Статистика",
        callback_data=StudentsCountCallbackData(),
    )
    builder.button(
        text="Список групп",
        callback_data=GroupsListCallbackData(),
    )
    builder.button(
        text="Удалить пользователя",
        callback_data=DeleteStudentCallbackData(),
    )
    builder.button(
        text="Сменить группу",
        callback_data=ChangeGroupCallbackData(),
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
        text="Отмена",
        callback_data=CancelActionCallbackData(),
    )
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def cancel_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Отмена",
        callback_data=CancelActionCallbackData(),
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
