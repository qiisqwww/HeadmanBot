from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable

__all__ = [
    "ShowAttendanceCallbackData",
]


class ShowAttendanceCallbackData(
    Expirerable,
    CallbackData,
    prefix="show_attendance",
):
    ...
