from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

__all__ = [
    "start_button",
    "restart_button",
]


def start_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="/start"))

    return builder.as_markup(resize_keyboard=True)


def restart_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="Начать регистрацию заново"))

    return builder.as_markup(resize_keyboard=True)
