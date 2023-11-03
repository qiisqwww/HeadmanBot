import datetime
import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from .messages import (
    ALREADY_HEADMAN_MESSAGE,
    ALREADY_REGISTERED_MESSAGE,
    MUST_BE_HEADMEN_MESSAGE,
    MUST_BE_REG_MESSAGE,
)
from .services import UsersService

__all__ = ["RegMiddleware", "HeadmenRegMiddleware", "HeadmenCommandsMiddleware", "CallbackMiddleware"]


class RegMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ) -> Any:
        logging.info("registration middleware started")

        user_id = event.from_user.id

        with UsersService() as con:
            if con.is_registered(user_id):
                await event.reply(ALREADY_REGISTERED_MESSAGE)
                logging.warning("middleware finished, already registered")
                return

        logging.info("registration middleware finished")
        return await handler(event, data)


class HeadmenRegMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
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


class HeadmenCommandsMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
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


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]
    ) -> Any:
        logging.info("callback middleware started")

        user_id = event.from_user.id
        flag = get_flag(data, "callback")

        if flag == "poll":
            with UsersService() as con:
                a = 60 * con.get_time(user_id).hour + con.get_time(user_id).minute + 90
                if a < datetime.datetime.now().time().hour * 60 + datetime.datetime.now().time().minute:
                    logging.warning("(poll) callback middleware finished, lesson was already started")
                    await event.message.edit_text("Вы не можете отметиться! Занятия уже начались!")
                    return

                logging.info("(poll) callback middleware finished")
                return await handler(event, data)

        if flag == "attendance":
            logging.info("(attendance) callback middlewre finished")
            return await handler(event, data)
