from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def load_attendance_kb(lessons: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text="Буду на всех", callback_data="attendance_all"),
               InlineKeyboardButton(text="Меня сегодня не будет", callback_data="attendance_none")]

    for i in range(len(lessons)):
        buttons.append(InlineKeyboardButton(text=f"Буду на {lessons[i][1]} {lessons[i][0]}", callback_data=f"attendance_{lessons[i]}"))

    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def load_void_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return builder.as_markup(resize_keyboard=True)