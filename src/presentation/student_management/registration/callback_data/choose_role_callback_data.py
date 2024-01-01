from aiogram.filters.callback_data import CallbackData

from src.domain.student_management import Role

__all__ = [
    "ChooseRoleCallbackData",
]


class ChooseRoleCallbackData(CallbackData, prefix="choose_role_callback"):  # type: ignore
    role: Role
