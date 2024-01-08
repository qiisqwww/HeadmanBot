from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from injector import Injector

from src.modules.common.application import Dependency

from ...contextes import ProfileUpdateContext, RegistrationContext

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectDependenciesMiddleware",
]


class InjectDependenciesMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        annotations = data["handler"].callback.__annotations__
        container: Injector = data["container"]

        if "state" in annotations:
            if annotations["state"] == RegistrationContext:
                data["state"] = RegistrationContext(data["state"])
            elif annotations["state"] == ProfileUpdateContext:
                data["state"] = ProfileUpdateContext(data["state"])

        for service_obj_name, service_type in annotations.items():
            if service_obj_name == "return" or not issubclass(service_type, Dependency):
                continue

            impl = container.get(service_type)
            data[service_obj_name] = impl

        return await handler(event, data)