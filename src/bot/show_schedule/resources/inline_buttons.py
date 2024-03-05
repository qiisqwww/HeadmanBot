from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = [
    "show_schedule_buttons",
]


def show_schedule_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Cегодня", callback_data="show_schedule_today")
    builder.button(text="Завтра", callback_data="show_schedule_tomorrow")
    # builder.button(text="Назад", callback_data="show_schedule_back")
    # builder.button(text="Текущая неделя")
    # builder.button(text="Текущий месяц")
    # builder.button(text="Текущий семестр")
    # builder.button(text="Назад")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
