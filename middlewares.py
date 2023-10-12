import logging

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from messages import ALREADY_REGISTERED_MESSAGE
from service import UsersService

class RegMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('middleware started')

        user_id = event.from_user.id

        with UsersService() as con:
            if con.is_registered(user_id):
                await event.reply(ALREADY_REGISTERED_MESSAGE)
                logging.warning("middleware finished, already registered")
                return

        logging.info("middleware finished")
        return await handler(event, data)

