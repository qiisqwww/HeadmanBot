from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AccessCallbackData",
]


class AccessCallbackData(CallbackData, prefix="confirm_access"):  # type: ignore
    telegram_id: int
    accepted: bool
