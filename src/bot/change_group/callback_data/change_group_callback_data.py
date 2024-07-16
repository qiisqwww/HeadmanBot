from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ChangeGroupCallbackData",
]


class ChangeGroupCallbackData(CallbackData, prefix="change_user's_group"):  # type: ignore
    ...
