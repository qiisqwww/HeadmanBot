from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from injector import Injector

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

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]


class InjectStudentMiddleware(BaseMiddleware):
    _must_be_registered: bool

    def __init__(self, must_be_registered: bool) -> None:
        super().__init__()
        self._must_be_registered = must_be_registered

    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        if event.from_user is None:
            return None

        container: Injector = data["container"]
        find_student_query = container.get(FindStudentByTelegramIdQuery)

        if data.get("student", None) is None:
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
