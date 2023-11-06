import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.messages import ALREADY_REGISTERED_MESSAGE
from src.services.student_service import StudentService

__all__ = ["RegMiddleware"]


class RegMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        logging.info("registration middleware started")

        user_id = event.from_user.id

        async with StudentService() as student_service:
            if await student_service.is_registered(user_id):
                await event.reply(ALREADY_REGISTERED_MESSAGE)
                logging.warning("middleware finished, already registered")
                return

        logging.info("registration middleware finished")

        return await handler(event, data)
