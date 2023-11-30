from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums import Role

__all__ = [
    "default_buttons",
    "start_button",
]


def start_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text="/start")

    builder.add(button)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def default_buttons(role: Role) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text="/faq")]

    if role == Role.HEADMAN:
        buttons.append(KeyboardButton(text="/getstat"))

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)
