from aiogram.filters.callback_data import CallbackData

__all__ = [
    "CancelActionCallbackData",
]


class CancelActionCallbackData(CallbackData, prefix="cancel_action"):  # type: ignore
    ...
