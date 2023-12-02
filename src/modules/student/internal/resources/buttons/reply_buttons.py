from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.kernel.role import Role

__all__ = [
    "default_buttons",
    "start_button",
    "remove_reply_buttons",
]


def remove_reply_buttons() -> ReplyKeyboardRemove:
    remove_markup = ReplyKeyboardRemove()

    return remove_markup


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
