from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.modules.common.infrastructure.container import Container

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectContainerMiddleware",
]


class InjectContainerMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        async with Container() as container:
            data["container"] = container
            return await handler(event, data)
