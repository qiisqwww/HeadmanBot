from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ShowStudentListCallbackData",
]


class ShowStudentListCallbackData(
    Expireable,
    CallbackData,
    prefix="show_students_list_headman",
):
    show_birthdate: bool = False
