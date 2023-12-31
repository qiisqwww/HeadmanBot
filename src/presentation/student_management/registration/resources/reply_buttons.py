from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.enums import TelegramCommand

__all__ = [
    "start_button",
    "restart_button",
]


def start_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=TelegramCommand.START))

    return builder.as_markup(resize_keyboard=True)


def restart_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=TelegramCommand.RESTART))

    return builder.as_markup(resize_keyboard=True)
