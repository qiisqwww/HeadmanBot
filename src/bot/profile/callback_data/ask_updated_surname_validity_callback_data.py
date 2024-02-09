from aiogram.filters.callback_data import CallbackData

__all__ = [
    "AskUpdatedSurnameValidityCallbackData",
]


class AskUpdatedSurnameValidityCallbackData(CallbackData, prefix="ask_last_name_for_update"):  # type: ignore
    is_field_correct: bool
