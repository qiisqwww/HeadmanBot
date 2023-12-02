from aiogram.filters.callback_data import CallbackData

from src.kernel.role import Role

__all__ = [
    "RoleCallbackData",
]


class RoleCallbackData(CallbackData, prefix="handle_role"):  # type: ignore
    role: Role
