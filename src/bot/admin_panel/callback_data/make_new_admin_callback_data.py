from aiogram.filters.callback_data import CallbackData

__all__ = [
    "MakeNewAdminCallbackData",
]


class MakeNewAdminCallbackData(CallbackData, prefix="make_new_user_to_admin"):  # type: ignore
    ...
