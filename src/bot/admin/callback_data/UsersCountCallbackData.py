from aiogram.filters.callback_data import CallbackData

__all__ = [
    "UsersCountCallbackData",
]


class UsersCountCallbackData(CallbackData, prefix="get_users_count"):  # type: ignore
    ...
