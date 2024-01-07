from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dependency_injector.containers import DeclarativeContainer

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectServicesMiddleware",
]


class InjectServicesMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        annotations = data["handler"].callback.__annotations__
        containers: list[DeclarativeContainer] = data["containers"]

        for container in containers:
            for service_obj_name, service_type in annotations.items():
                if service_obj_name == "return":
                    continue

                for provider in container.traverse():
                    if provider.provides == service_type:
                        data[service_obj_name] = provider.async_()

        return await handler(event, data)
