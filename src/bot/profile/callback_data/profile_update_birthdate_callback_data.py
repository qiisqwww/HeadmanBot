from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ProfileUpdateBirthdateCallbackData",
]


class ProfileUpdateBirthdateCallbackData(CallbackData, prefix="profile_update_birthdate_prefix"):  # type: ignore
    ...
