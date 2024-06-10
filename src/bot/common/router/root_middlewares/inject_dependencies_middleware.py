from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectDependenciesMiddleware",
]


class InjectDependenciesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: HandlerType,
        event: EventType,
        data: dict[str, Any],
    ) -> Any:
        annotations = data["handler"].callback.__annotations__
        container = data["container"]

        if "state" in annotations and annotations["state"] is not FSMContext:
            data["state"] = annotations["state"](data["state"])

        for service_obj_name, service_type in annotations.items():
            if service_obj_name == "return":
                continue

            if not container.has_dependency(service_type):
                continue

            impl = container.get_dependency(service_type)
            data[service_obj_name] = impl

        return await handler(event, data)
