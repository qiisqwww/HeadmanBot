from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AskFullnameValidityCallbackData",
]


class AskFullnameValidityCallbackData(CallbackData, prefix="ask_fullname_for_headman"):  # type: ignore
    is_fullname_correct: bool
