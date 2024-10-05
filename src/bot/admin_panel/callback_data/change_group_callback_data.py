from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ChangeGroupCallbackData",
]


class ChangeGroupCallbackData(CallbackData, prefix="change group (only for admins)"):  # type: ignore
    ...
