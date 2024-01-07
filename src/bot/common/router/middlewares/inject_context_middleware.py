from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ...contextes import ProfileUpdateContext, RegistrationContext

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectContextMiddleware",
]


class InjectContextMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        annotations = data["handler"].callback.__annotations__

        if "state" in annotations:
            if annotations["state"] == RegistrationContext and not isinstance(data["state"], RegistrationContext):
                data["state"] = RegistrationContext(data["state"])

            elif annotations["state"] == ProfileUpdateContext and not isinstance(data["state"], ProfileUpdateContext):
                data["state"] = ProfileUpdateContext(data["state"])

        return await handler(event, data)
