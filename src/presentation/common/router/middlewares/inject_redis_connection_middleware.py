from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Update
from loguru import logger
from redis.asyncio import Redis

from src.infrastructure.common.database import get_redis_pool

__all__ = [
    "InjectRedisConnectionMiddleware",
]

HandlerType: TypeAlias = Callable[[Update, dict[str, Any]], Awaitable[Any]]


class InjectRedisConnectionMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Update, data: dict[str, Any]) -> Any:
        logger.trace("Inject redis connection middleware started.")

        if data.get("redis_con", None) is not None:
            logger.trace("Inject redis connection middleware finished.")
            return await handler(event, data)

        pool = get_redis_pool()
        async with Redis(connection_pool=pool) as redis_con:
            data["redis_con"] = redis_con
            logger.trace("Inject redis connection middleware finished.")
            return await handler(event, data)
