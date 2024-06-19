from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ScheduleWeekCallbackData",
]


class ScheduleWeekCallbackData(
    Expireable,
    CallbackData,
    prefix="choose_schedule_week_callback_data",
):
    weeks_to_add: int
