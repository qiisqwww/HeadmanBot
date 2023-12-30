from aiogram.filters.callback_data import CallbackData


__all__ = [
    "GetBackToProfileCallbackData",
]


class GetBackToProfileCallbackData(CallbackData, prefix="back_to_profile"):  # type: ignore
    ...
