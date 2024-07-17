from aiogram.filters.callback_data import CallbackData

__all__ = [
    "QuitGroupCallbackData",
]


class QuitGroupCallbackData(CallbackData, prefix="quit_user's_group"):  # type: ignore
    ...
