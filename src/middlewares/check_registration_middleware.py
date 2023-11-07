from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from src.messages import ALREADY_REGISTERED_MESSAGE, MUST_BE_REG_MESSAGE
from src.services import StudentService

__all__ = [
    "CheckRegistrationMiddleware",
]

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]


class CheckRegistrationMiddleware(BaseMiddleware):
    _must_be_registered: bool

    def __init__(self, must_be_registered: bool) -> None:
        self._must_be_registered = must_be_registered
        super().__init__()

    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        logger.info("registration middleware started")

        if event.from_user is None:
            return

        user_id = event.from_user.id

        async with StudentService() as student_service:
            is_registered = await student_service.is_registered(user_id)

        if is_registered != self._must_be_registered and not self._must_be_registered:
            await event.reply(ALREADY_REGISTERED_MESSAGE)
            logger.trace("middleware finished, already registered")
            return

        if is_registered != self._must_be_registered and self._must_be_registered:
            await event.reply(MUST_BE_REG_MESSAGE)
            logger.trace("middleware finished, must be registered")
            return

        logger.trace("registration middleware finished")
        return await handler(event, data)
