from aiogram.filters.callback_data import CallbackData

__all__ = [
    "DeleteUserCallbackData",
]


class DeleteUserCallbackData(CallbackData, prefix="delete_user_callback_data"):  # type: ignore
    ...
