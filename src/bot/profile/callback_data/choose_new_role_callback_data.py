from aiogram.filters.callback_data import CallbackData

from src.modules.student_management.domain import Role

__all__ = [
    "ChooseNewRoleCallbackData",
]


class ChooseNewRoleCallbackData(CallbackData, prefix="choose_new_role"):  # type: ignore
    role: Role
