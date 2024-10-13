from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.common.database import DbContext
from src.common.use_case import UseCase

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
        pool = data["pool"]
        async with DbContext(pool) as con:
            annotations = data["handler"].callback.__annotations__

            if "state" in annotations and annotations["state"] is not FSMContext:
                data["state"] = annotations["state"](data["state"])

            for service_obj_name, service_type in annotations.items():
                if service_obj_name == "return":
                    continue

                if issubclass(service_type, UseCase):
                    impl = service_type(con=con)
                    data[service_obj_name] = impl

            return await handler(event, data)
