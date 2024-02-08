from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AskUpdatedNameValidityCallbackData",
]


class AskUpdatedNameValidityCallbackData(CallbackData, prefix="ask_name_for_update"):  # type: ignore
    is_field_correct: bool
