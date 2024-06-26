from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ScheduleCertainDayCallbackData",
]


class ScheduleCertainDayCallbackData(
    Expireable,
    CallbackData,
    prefix="input_certain_date_to_get_schedule",
):
    ...
