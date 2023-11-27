from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from src.database import get_pool

__all__ = [
    "InjectDBConnectionMiddleware",
]

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]


class InjectDBConnectionMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler, event, data) -> Any:
        logger.trace("Inject database connection middleware started.")

        pool = await get_pool()
        async with pool.acquire() as con:
            data["con"] = con
            logger.trace("Inject database connection middleware finished.")
            return await handler(event, data)
