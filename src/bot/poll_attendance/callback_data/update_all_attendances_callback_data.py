from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable
from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAllAttendancesCallbackData",
]


class UpdateAllAttendancesCallbackData(
    Expirerable, CallbackData, prefix="update_all_attendace_prefix",
):
    new_status: VisitStatus
