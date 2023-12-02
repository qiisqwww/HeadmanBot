from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Update
from loguru import logger
from redis.asyncio import Redis

from ...external.database import get_redis_pool

__all__ = [
    "InjectRedisConnectionMiddleware",
]

HandlerType: TypeAlias = Callable[[Update, dict[str, Any]], Awaitable[Any]]


class InjectRedisConnectionMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Update, data: dict[str, Any]) -> Any:
        logger.trace("Inject redis connection middleware started.")

        pool = get_redis_pool()
        async with Redis(connection_pool=pool) as redis_con:
            data["redis_con"] = redis_con
            logger.trace("Inject redis connection middleware finished.")
            return await handler(event, data)
