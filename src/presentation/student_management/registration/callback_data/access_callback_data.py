from aiogram.filters.callback_data import CallbackData

from src.dto.models import StudentId

__all__ = [
    "AccessCallbackData",
]


class AccessCallbackData(CallbackData, prefix="confirm_access"):  # type: ignore
    accepted: bool
    student_id: StudentId