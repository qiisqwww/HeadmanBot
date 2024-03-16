from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable

__all__ = [
    "SetViceHeadmanCallbackData",
]


class SetViceHeadmanCallbackData(
    Expirerable,
    CallbackData,
    prefix="set_vice_headman",
):
    ...
