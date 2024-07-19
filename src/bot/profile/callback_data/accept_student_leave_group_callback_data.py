from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AcceptStudentLeaveGroupCallbackData",
]


class AcceptStudentLeaveGroupCallbackData(CallbackData, prefix="confirm_leave_group"):  # type: ignore
    telegram_id: int
    accepted: bool
