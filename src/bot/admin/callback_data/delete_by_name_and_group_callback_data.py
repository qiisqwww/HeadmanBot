from aiogram.filters.callback_data import CallbackData

__all__ = [
    "DeleteByNameAndGroupCallbackData",
]


class DeleteByNameAndGroupCallbackData(CallbackData, prefix="delete_user_by_name_and_group_callback_data"):  # type: ignore
    ...
