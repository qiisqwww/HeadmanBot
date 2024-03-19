from aiogram.filters.callback_data import CallbackData

from src.bot.common.expirable import Expirerable

__all__ = [
    "ChooseStudentToDowngradeCallbackData",
]


class ChooseStudentToDowngradeCallbackData(
    Expirerable,
    CallbackData,
    prefix="choose_student_for_downgrading_role",
):
    student_id: int
    telegram_id: int
