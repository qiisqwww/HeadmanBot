from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.show_schedule.callback_data import (
    ScheduleWeekCallbackData,
    ScheduleDayCallbackData
)

__all__ = [
    "show_choose_period_buttons",
    "show_choose_day_buttons"
]


def show_choose_period_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Сегодня", callback_data=ScheduleDayCallbackData(chosen_day=datetime.today()))
    builder.button(text="Текущая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=0))
    builder.button(text="Следующая неделя", callback_data=ScheduleWeekCallbackData(weeks_to_add=1))
    builder.button(text="Неделя после следующей", callback_data=ScheduleWeekCallbackData(weeks_to_add=2))

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


def show_choose_day_buttons(week_to_add: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    day_of_week = datetime.today() + timedelta(days=7*week_to_add)
    week_runner = day_of_week - timedelta(days=day_of_week.weekday() % 7)
    for i in range(7):
        builder.button(text=week_runner.date().__str__(), callback_data=ScheduleDayCallbackData(chosen_day=week_runner))
        week_runner += timedelta(days=1)
    builder.button(text="Вернуться назад", callback_data="back_to_week_choice_list")

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
