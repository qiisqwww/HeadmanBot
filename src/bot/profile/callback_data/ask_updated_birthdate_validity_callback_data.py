from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AskUpdatedBirthdateValidityCallbackData",
]


class AskUpdatedBirthdateValidityCallbackData(CallbackData, prefix="ask_birthdate_for_update"):  # type: ignore
    is_field_correct: bool
