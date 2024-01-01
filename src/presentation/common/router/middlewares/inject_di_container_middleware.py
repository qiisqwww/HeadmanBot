from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from loguru import logger

from src.infrastructure.container import HeadmanDIContainer

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectDIContainerMiddleware",
]


class InjectDIContainerMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        data["container"] = HeadmanDIContainer(db_con=data["postgres_con"])

        return await handler(event, data)
