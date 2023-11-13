from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = ["load_void_button"]


def load_void_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup(resize_keyboard=True)