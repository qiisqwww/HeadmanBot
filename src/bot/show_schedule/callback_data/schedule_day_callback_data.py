import datetime

from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ScheduleDayCallbackData",
]


class ScheduleDayCallbackData(
    Expireable,
    CallbackData,
    prefix="choose_schedule_day_callback_data",
):
    chosen_day: datetime.date
