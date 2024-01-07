from aiogram.filters.callback_data import CallbackData

from src.modules.student_management.domain import Role

__all__ = [
    "ChooseRoleCallbackData",
]


class ChooseRoleCallbackData(CallbackData, prefix="choose_role_callback"):  # type: ignore
    role: Role
