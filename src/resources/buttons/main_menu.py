from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums import Role

__all__ = [
    "main_menu",
]


def main_menu(role: Role) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text="Помощь")]

    if role >= Role.VICE_HEADMAN:
        buttons.append(KeyboardButton(text="Узнать посещаемость"))

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)
