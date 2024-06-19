from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable
from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(
    Expireable,
    CallbackData,
    prefix="update_attendace_prefix",
):
    attendance_id: int
    new_status: VisitStatus
