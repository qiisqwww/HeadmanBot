from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ProfileUpdateNameCallbackData",
]


class ProfileUpdateNameCallbackData(CallbackData, prefix="profile_update_name_prefix"):  # type: ignore
    ...
