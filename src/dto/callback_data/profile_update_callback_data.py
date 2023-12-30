from aiogram.filters.callback_data import CallbackData

from src.enums import ProfileField

__all__ = [
    "ProfileUpdateCallbackData",
]


class ProfileUpdateCallbackData(CallbackData, prefix="profile_update_prefix"):  # type: ignore
    updating_data: ProfileField
