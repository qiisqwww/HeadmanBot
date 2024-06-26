from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "UnsetViceHeadmanCallbackData",
]


class UnsetViceHeadmanCallbackData(
    Expireable,
    CallbackData,
    prefix="unset_vice_headman",
):
    ...
