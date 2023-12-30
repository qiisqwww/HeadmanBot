from aiogram.filters.callback_data import CallbackData

from src.enums import ProfileField

__all__ = [
    "AskUpdatedFieldValidityCallbackData",
]


class AskUpdatedFieldValidityCallbackData(CallbackData, prefix="ask_field_for_update"):  # type: ignore
    is_field_correct: bool
    field_type: ProfileField

