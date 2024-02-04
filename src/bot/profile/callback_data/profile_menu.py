from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ProfileUpdateCallbackData",
]


class ProfileUpdateCallbackData(CallbackData, prefix="profile_update_prefix"):  # type: ignore
    ...
