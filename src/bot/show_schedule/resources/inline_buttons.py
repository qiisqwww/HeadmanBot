from datetime import datetime
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.show_schedule.callback_data import (
    ScheduleWeekCallbackData,
    ScheduleDayCallbackData
)

__all__ = [
    "show_schedule_buttons",
    "show_choose_period_buttons"
]


def show_schedule_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Cегодня", callback_data="show_schedule_today")
    builder.button(text="Завтра", callback_data="show_schedule_tomorrow")
    # builder.button(text="Текущая неделя")
    # builder.button(text="Следующая неделя")
    # builder.button(text="Текущий месяц")
    # builder.button(text="Текущий семестр")
    # builder.button(text="Назад", callback_data="show_schedule_back")

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def show_choose_period_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Сегодня", callback_data=ScheduleDayCallbackData(chosen_day=datetime.today()))
    builder.button(text="Текущая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=0))
    builder.button(text="Следующая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=1))
    builder.button(text="Неделя после следующей", callback_data=ScheduleWeekCallbackData(weeks_to_add=2))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
