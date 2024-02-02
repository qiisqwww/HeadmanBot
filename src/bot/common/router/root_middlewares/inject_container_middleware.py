from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectContainerMiddleware",
]


class InjectContainerMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        project_container = data["project_container"]

        async with project_container() as container:
            logger.error(type(project_container))
            data["container"] = container
            return await handler(event, data)
