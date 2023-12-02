from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Update
from loguru import logger

from ...external.database import get_postgres_pool

__all__ = [
    "InjectPostgresMiddleware",
]

HandlerType: TypeAlias = Callable[[Update, dict[str, Any]], Awaitable[Any]]


class InjectPostgresMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Update, data: dict[str, Any]) -> Any:
        logger.trace("Inject database connection middleware started.")

        pool = await get_postgres_pool()
        async with pool.acquire() as con:
            data["postgres_con"] = con
            logger.trace("Inject database connection middleware finished.")
            return await handler(event, data)
