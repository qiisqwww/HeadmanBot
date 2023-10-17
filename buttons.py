from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def load_attendance_kb(lessons_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    buttons = [InlineKeyboardButton(text="Буду на всех", callback_data="attendance_all"),
               InlineKeyboardButton(text="Меня сегодня не будет", callback_data="attendance_none")]

    lesson_buttons = [InlineKeyboardButton(text="Не буду на первой паре", callback_data="attendance_1"),
                      InlineKeyboardButton(text="Не буду на второй паре", callback_data="attendance_2"),
                      InlineKeyboardButton(text="Не буду на третьей паре", callback_data="attendance_3"),
                      InlineKeyboardButton(text="Не буду на четвертой паре", callback_data="attendance_4")]

    for i in range(lessons_count):
        buttons.append(lesson_buttons[i])

    builder.add(*buttons)
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
