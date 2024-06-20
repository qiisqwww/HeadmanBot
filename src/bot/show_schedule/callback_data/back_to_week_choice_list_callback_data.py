from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "BackToWeekChoiceListCallbackData",
]


class BackToWeekChoiceListCallbackData(
    Expireable,
    CallbackData,
    prefix="back_to_week_choice_list",
):
    ...
