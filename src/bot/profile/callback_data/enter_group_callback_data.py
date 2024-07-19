from aiogram.filters.callback_data import CallbackData

__all__ = [
    "EnterGroupCallbackData",
]


class EnterGroupCallbackData(CallbackData, prefix="enter_new_group"):  # type: ignore
    ...
