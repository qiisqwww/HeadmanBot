from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag
from loguru import logger

from src.services.redis_service import RedisService

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]

__all__ = ["ThrottlingMiddleware"]


class ThrottlingMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        user_id = str(event.from_user.id)

        void = get_flag(data, "void")
        if void:
            return

        with RedisService() as storage:
            user_activity = storage.get_user_throttling(user_id)
            if not user_activity:
                storage.set_user_throttling(user_id)
                return await handler(event, data)

            if int(user_activity) >= 10:
                return

            storage.increase_user_throttling(user_id)
        return await handler(event, data)