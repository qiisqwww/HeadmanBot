from aiogram.filters.callback_data import CallbackData

__all__ = [
    "SureToLeaveGroupCallbackData",
]


class SureToLeaveGroupCallbackData(CallbackData, prefix="sure_to_leave_or_not"):  # type: ignore
    is_user_sure: bool
