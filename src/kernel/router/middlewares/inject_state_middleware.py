from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from loguru import logger

from src.handlers.finite_state.registration.registration_context import (
    RegistrationContext,
)

HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "InjectStateMiddleware",
]


class InjectStateMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: TelegramObject, data: dict[str, Any]) -> Any:
        annotations = data["handler"].spec.annotations

        if "state" in annotations:
            if annotations["state"] == RegistrationContext and not isinstance(data["state"], RegistrationContext):
                data["state"] = RegistrationContext(data["state"])

        return await handler(event, data)
