from datetime import date

from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ScheduleDateCallbackData",
]


class ScheduleDateCallbackData(
    Expireable,
    CallbackData,
    prefix="choose_schedule_day_callback_data",
):
    chosen_day: date
    weeks_to_add: int
