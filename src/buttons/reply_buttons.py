from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

__all__ = [
    "default_buttons",
    "start_button",
    "university_list_buttons",
    "role_buttons"
]


def start_button() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    button = KeyboardButton(text='/start')

    builder.add(button)
    return builder.as_markup(resize_keyboard=True,
                             one_time_keyboard=True)


def default_buttons(is_headman: bool) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text="/faq")]

    if is_headman: buttons.append(KeyboardButton(text="/getstat"))

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)


def university_list_buttons() -> ReplyKeyboardMarkup:
    """we need to generate buttons list according to registrated universities, so this code is just for
       example of work"""
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text='МИРЭА'), KeyboardButton(text='Бауманка')]

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)


def role_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text="Я студент"), KeyboardButton(text="Я староста")]

    builder.add(*buttons)
    return builder.as_markup(resize_keyboard=True)
