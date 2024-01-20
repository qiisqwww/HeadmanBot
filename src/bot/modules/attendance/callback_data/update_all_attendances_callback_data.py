from aiogram.filters.callback_data import CallbackData

from src.modules.attendance.domain.enums.visit_status import VisitStatus

__all__ = [
    "UpdateAllAttendancesCallbackData",
]


class UpdateAllAttendancesCallbackData(CallbackData, prefix="update_all_attendace_prefix"):  # type: ignore
    new_status: VisitStatus
    # day_of_poll: date