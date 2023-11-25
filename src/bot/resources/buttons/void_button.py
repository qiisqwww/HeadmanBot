from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = [
    "inline_void_button",
    "remove_reply_buttons",
]


def inline_void_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup(resize_keyboard=True)


def remove_reply_buttons() -> ReplyKeyboardRemove:
    remove_markup = ReplyKeyboardRemove()

    return remove_markup
