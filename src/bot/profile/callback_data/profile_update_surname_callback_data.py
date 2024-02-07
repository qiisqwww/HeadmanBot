from aiogram.filters.callback_data import CallbackData

__all__ = [
    "ProfileUpdateSurnameCallbackData",
]


class ProfileUpdateSurnameCallbackData(CallbackData, prefix="profile_update_surname_prefix"):  # type: ignore
    ...
