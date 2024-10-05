from aiogram.filters.callback_data import CallbackData

__all__ = [
    "DeleteByTGIDCallbackData",
]


class DeleteByTGIDCallbackData(CallbackData, prefix="delete_user_by_tg_id_callback_data"):  # type: ignore
    ...
