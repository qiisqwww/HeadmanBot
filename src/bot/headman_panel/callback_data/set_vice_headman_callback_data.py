from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "SetViceHeadmanCallbackData",
]


class SetViceHeadmanCallbackData(
    Expireable,
    CallbackData,
    prefix="set_vice_headman",
):
    ...
