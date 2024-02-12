
from datetime import date

from aiogram.filters.callback_data import CallbackData

from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAttendanceCallbackData",
]


class UpdateAttendanceCallbackData(CallbackData, prefix="update_attendace_prefix"):  # type: ignore
    attendance_id: int
    new_status: VisitStatus
    day_of_poll: date
