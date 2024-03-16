from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.modules.student_management.domain import Role

from ..command_filter import TelegramCommand

__all__ = [
    "main_menu",
]


def main_menu(role: Role) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text=TelegramCommand.HELP),
        KeyboardButton(text=TelegramCommand.PROFILE),
        KeyboardButton(text=TelegramCommand.SHOW_SCHEDULE),
    ]

    if role >= Role.VICE_HEADMAN:
        buttons.append(KeyboardButton(text=TelegramCommand.GROUP_PANEL))

    if role == Role.ADMIN:
        buttons.append(KeyboardButton(text=TelegramCommand.ADMIN))

    builder.add(*buttons)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
