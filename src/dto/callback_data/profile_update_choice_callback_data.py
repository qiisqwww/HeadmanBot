from aiogram.filters.callback_data import CallbackData

from src.enums import ProfileField

__all__ = [
    "ProfileUpdateChoiceCallbackData",
]


class ProfileUpdateChoiceCallbackData(CallbackData, prefix="profile_update_choice_prefix"):  # type: ignore
    updating_data: ProfileField | None = None
