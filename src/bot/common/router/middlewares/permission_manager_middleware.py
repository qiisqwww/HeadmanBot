from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.modules.edu_info.application.queries import FetchUniTimezonByGroupIdQuery
from src.modules.student_management.domain import Role
from .templates import YOU_DONT_HAVE_ENOUGH_RIGHTS_TEMPLATE

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "PermissionManagerMiddleware",
]

if TYPE_CHECKING:
    from src.common.infrastructure import Container


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

        container: Container = data["container"]
        fetch_timezone_query = container.get_dependency(FetchUniTimezonByGroupIdQuery)

        timezone = await fetch_timezone_query.execute(student.group_id)
        data["timezone"] = timezone

        return await handler(event, data)
