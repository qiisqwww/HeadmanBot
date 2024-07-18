from aiogram.filters.callback_data import CallbackData

__all__ = [
    "LeaveGroupCallbackData",
]


class LeaveGroupCallbackData(CallbackData, prefix="quit_user's_group"):  # type: ignore
    ...
