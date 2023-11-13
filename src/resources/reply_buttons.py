from aiogram.types import (KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def load_headman_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text="/ask"),
               KeyboardButton(text='/faq')]

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)


def load_become_headman_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text="Стать старостой")

    builder.add(button)
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)
