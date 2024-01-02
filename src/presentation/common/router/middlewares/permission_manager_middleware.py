from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.domain.student_management.enums import Role

HandlerType: TypeAlias = Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "PermissionManagerMiddleware",
]


class PermissionManagerMiddleware(BaseMiddleware):
    _min_role: Role

    def __init__(self, min_role: Role) -> None:
        self._min_role = min_role
        super().__init__()

    async def __call__(self, handler: HandlerType, event: Message | CallbackQuery, data: dict[str, Any]) -> Any:
        student = data["student"]

        if student.role < self._min_role:
            await event.answer("У вас недостаточно прав для выполнения данной команды")
            return

        return await handler(event, data)
