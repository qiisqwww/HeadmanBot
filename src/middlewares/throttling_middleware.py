from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from loguru import logger

from src.bot.services import RedisService

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

        async with RedisService() as storage:
            user_activity = await storage.get_user_throttling(user_id)
            if not user_activity:
                await storage.set_user_throttling(user_id)
                return await handler(event, data)

            if int(user_activity) >= 10:
                return

            await storage.increase_user_throttling(user_id)
        return await handler(event, data)
