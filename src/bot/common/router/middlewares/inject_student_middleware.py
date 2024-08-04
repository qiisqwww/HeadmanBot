from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.common.router.middlewares.templates import (
    ALREADY_REGISTERED_TEMPLATE,
    MUST_BE_REG_TEMPLATE,
)
from src.modules.student_management.application.queries import (
    FindStudentByTelegramIdQuery,
)

__all__ = [
    "InjectStudentMiddleware",
]

if TYPE_CHECKING:
    from src.modules.common.infrastructure.container import Container

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]


class InjectStudentMiddleware(BaseMiddleware):
    _must_be_registered: bool

    def __init__(self, must_be_registered: bool) -> None:
        super().__init__()
        self._must_be_registered = must_be_registered

    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        if event.from_user is None:
            return None

        container: Container = data["container"]
        find_student_query = container.get_dependency(FindStudentByTelegramIdQuery)

        if data.get("student") is None:
            student = await find_student_query.execute(event.from_user.id)
        else:
            student = data["student"]

        is_registered = student is not None

        if is_registered != self._must_be_registered and not self._must_be_registered:
            return await event.answer(ALREADY_REGISTERED_TEMPLATE)

        if is_registered != self._must_be_registered and self._must_be_registered:
            return await event.answer(MUST_BE_REG_TEMPLATE)

        data["student"] = student

        return await handler(event, data)
