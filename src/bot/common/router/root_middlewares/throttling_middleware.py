from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.modules.utils.throttling.application.commands import CanPerformActionCommand

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "ThrottlingMiddleware",
]

if TYPE_CHECKING:
    from injector import Injector


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        if event.from_user is None:
            return None

        telegram_id = str(event.from_user.id)

        if get_flag(data, "void"):
            logger.error("Void event.")
            return None

        container: Injector = data["container"]

        can_perform_action_command = container.get(CanPerformActionCommand)
        can_perform_action = await can_perform_action_command.execute(telegram_id)

        if can_perform_action:
            return await handler(event, data)
        return None
