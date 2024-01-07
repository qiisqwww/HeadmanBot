from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = [
    "void_inline_buttons",
]


def void_inline_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup(resize_keyboard=True)
