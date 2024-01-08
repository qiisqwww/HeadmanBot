from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from injector import Injector

from src.modules.common.application import Dependency

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectServicesMiddleware",
]


class InjectServicesMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        annotations = data["handler"].callback.__annotations__
        container: Injector = data["container"]

        for service_obj_name, service_type in annotations.items():
            if service_obj_name == "return" or not issubclass(service_type, Dependency):
                continue

            impl = container.get(service_type)
            data[service_obj_name] = impl

        return await handler(event, data)
