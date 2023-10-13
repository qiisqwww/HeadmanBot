from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def load_start_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text = "/start"))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)