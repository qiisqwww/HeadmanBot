import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.messages import (
    MUST_BE_HEADMEN_MESSAGE,
    MUST_BE_REG_MESSAGE,
)
from src.services import UsersService

__all__ = ["HeadmanCommandsMiddleware"]


class HeadmanCommandsMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        logging.info("headmen commands middleware started")

        user_id = event.from_user.id

        with UsersService() as con:
            if not con.is_registered(user_id):
                await event.reply(MUST_BE_REG_MESSAGE)
                logging.warning("headmen commands middleware finished, user must be registered")
                return

            if not con.is_headmen(user_id):
                await event.reply(MUST_BE_HEADMEN_MESSAGE)
                logging.warning("headmen commands middleware finished, user must me headman to use this command")
                return

            logging.info("headmen commands middleware finished")
            return await handler(event, data)
