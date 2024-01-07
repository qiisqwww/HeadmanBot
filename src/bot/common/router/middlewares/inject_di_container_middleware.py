from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dependency_injector.containers import DeclarativeContainer

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
AssembleContainer: TypeAlias = Callable[[], Awaitable[list[DeclarativeContainer]]]

__all__ = [
    "InjectDIContainerMiddleware",
]


class InjectDIContainerMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        assemble_project_containers: AssembleContainer = data["assemble_project_containers"]
        data["containers"] = await assemble_project_containers()

        return await handler(event, data)
