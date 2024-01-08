from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery, Message
from injector import Injector
from loguru import logger

from ..throttling_service import ThrottlingService

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "ThrottlingMiddleware",
]


class ThrottlingMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        if event.from_user is None:
            return None

        telegram_id = str(event.from_user.id)

        if get_flag(data, "void"):
            logger.error("Void event.")
            return

        container: Injector = data["container"]

        throttling_service = container.get(ThrottlingService)
        user_activity = await throttling_service.get_user_throttling(telegram_id)

        if not user_activity:
            await throttling_service.set_user_throttling(telegram_id)
            return await handler(event, data)

        if int(user_activity) >= 10:
            return

        await throttling_service.increase_user_throttling(telegram_id)
        return await handler(event, data)
