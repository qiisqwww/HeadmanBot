from aiogram.filters.callback_data import CallbackData

__all__ = [
    "GetBackCallbackData",
]


class GetBackCallbackData(CallbackData, prefix="get_back"):  # type: ignore
    ...
