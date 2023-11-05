import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.messages import (
    ALREADY_HEADMAN_MESSAGE,
    MUST_BE_REG_MESSAGE,
)
from src.services import UsersService

__all__ = ["HeadmanRegMiddleware"]


class HeadmanRegMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        logging.info("headmen middleware started")

        user_id = event.from_user.id

        with UsersService() as con:
            if not con.is_registered(user_id):
                await event.reply(MUST_BE_REG_MESSAGE)
                logging.warning("headmen reg middleware finished, user must be registered")
                return

            if con.is_headmen(user_id):
                await event.reply(ALREADY_HEADMAN_MESSAGE)
                logging.warning("headmen reg middleware finished, already registered as headmen")
                return

        logging.info("headmen reg middleware finished")
        return await handler(event, data)
