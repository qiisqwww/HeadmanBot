from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable
from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(
    Expirerable,
    CallbackData,
    prefix="update_attendace_prefix",
):
    attendance_id: int
    new_status: VisitStatus
