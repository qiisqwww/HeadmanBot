from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable
from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAllAttendancesCallbackData",
]


class UpdateAllAttendancesCallbackData(
    Expireable, CallbackData, prefix="update_all_attendace_prefix",
):
    new_status: VisitStatus
