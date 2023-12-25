from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums import Role, TelegramCommand

__all__ = [
    "main_menu",
]


def main_menu(role: Role) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=TelegramCommand.HELP)]

    if role >= Role.VICE_HEADMAN:
        buttons.append(KeyboardButton(text=TelegramCommand.GET_ATTENDANCE))

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)
