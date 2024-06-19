from aiogram.filters.callback_data import CallbackData

from src.bot.common.expireable import Expireable

__all__ = [
    "ChooseStudentToDowngradeCallbackData",
]


class ChooseStudentToDowngradeCallbackData(
    Expireable,
    CallbackData,
    prefix="choose_student_for_downgrading_role",
):
    student_id: int
    telegram_id: int
