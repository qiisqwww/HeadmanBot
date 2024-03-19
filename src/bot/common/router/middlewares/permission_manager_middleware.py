from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.modules.edu_info.application.queries import FetchUniTimezonByGroupIdQuery
from src.modules.student_management.domain import Role

from .templates import YOU_DONT_HAVE_ENOUGH_RIGHTS_TEMPLATE

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "PermissionManagerMiddleware",
]

if TYPE_CHECKING:
    from injector import Injector


class PermissionManagerMiddleware(BaseMiddleware):
    _min_role: Role

    def __init__(self, min_role: Role) -> None:
        self._min_role = min_role
        super().__init__()

    async def __call__(
        self,
        handler: HandlerType,
        event: EventType,
        data: dict[str, Any],
    ) -> Any:
        student = data["student"]

        if student.role < self._min_role:
            await event.answer(YOU_DONT_HAVE_ENOUGH_RIGHTS_TEMPLATE)
            return None

        container: Injector = data["container"]
        fetch_timezone_query = container.get(FetchUniTimezonByGroupIdQuery)

        timezone = await fetch_timezone_query.execute(student.group_id)
        data["timezone"] = timezone

        return await handler(event, data)
