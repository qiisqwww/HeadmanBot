from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from loguru import logger

from src.kernel.services import ThrottlingService

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "ThrottlingMiddleware",
]


class ThrottlingMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        if event.from_user is None:
            return None

        user_id = str(event.from_user.id)

        void = get_flag(data, "void")
        if void:
            return

        throttling_service = ThrottlingService(data["redis_con"])
        user_activity = await throttling_service.get_user_throttling(user_id)
        if not user_activity:
            await throttling_service.set_user_throttling(user_id)
            return await handler(event, data)

        if int(user_activity) >= 10:
            return

        await throttling_service.increase_user_throttling(user_id)
        return await handler(event, data)