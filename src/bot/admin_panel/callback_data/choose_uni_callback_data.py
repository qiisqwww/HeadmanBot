from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ChooseUniCallbackData",
]


class ChooseUniCallbackData(CallbackData, prefix="choose new uni (only for admins)"):  # type: ignore
    ...
