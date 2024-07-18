from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AcceptRegistrationCallbackData",
]


class AcceptRegistrationCallbackData(CallbackData, prefix="confirm_access"):  # type: ignore
    telegram_id: int
    accepted: bool
