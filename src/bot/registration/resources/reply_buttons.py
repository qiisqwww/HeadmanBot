from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.bot.common import TelegramCommand

__all__ = [
    "restart_button",
]


def restart_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text=TelegramCommand.RESTART))

    return builder.as_markup(resize_keyboard=True)
