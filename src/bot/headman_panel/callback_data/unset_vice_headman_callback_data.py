from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable

__all__ = [
    "UnsetViceHeadmanCallbackData",
]


class UnsetViceHeadmanCallbackData(
    Expirerable,
    CallbackData,
    prefix="unset_vice_headman",
):
    ...
