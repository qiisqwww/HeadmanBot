from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AcceptStudentEnterGroupCallbackData",
]


class AcceptStudentEnterGroupCallbackData(CallbackData, prefix="confirm_enter_group"):  # type: ignore
    telegram_id: int
    accepted: bool
