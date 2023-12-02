from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.kernel.base import PostgresService, RedisService

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectServices",
    "ServiceClass",
]

ServiceClass: TypeAlias = type[RedisService] | type[PostgresService]


class InjectServices(BaseMiddleware):
    _deps: dict[str, ServiceClass]

    def __init__(self, **deps: ServiceClass) -> None:
        self._deps = deps

    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        for service_obj_name, service_class in self._deps.items():
            if issubclass(service_class, PostgresService):
                data[service_obj_name] = service_class(data["postgres_con"])
            else:
                data[service_obj_name] = service_class(data["redis_con"])

        return await handler(event, data)
