from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.auth.callback_data import RoleCallbackData, UniversityCallbackData
from src.dto import University
from src.enums import Role


def university_list_buttons(universities: Iterable[University]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uni in universities:
        builder.button(text=uni.name, callback_data=UniversityCallbackData(university_alias=uni.alias))

    return builder.as_markup(resize_keyboard=True)


def role_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Я студент", callback_data=RoleCallbackData(role=Role.STUDENT))
    builder.button(text="Я староста", callback_data=RoleCallbackData(role=Role.HEADMAN))

    return builder.as_markup(resize_keyboard=True)
