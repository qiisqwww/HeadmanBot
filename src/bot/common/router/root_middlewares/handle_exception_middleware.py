from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from .templates import SOMETHING_WENT_WRONG_TEMPLATE

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "HandleExceptionMiddleware",
]


class HandleExceptionMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: EventType, data: dict[str, Any]) -> Any:
        try:
            return await handler(event, data)

        except Exception as e:
            logger.exception(e)

            if isinstance(event, Message):
                return await event.answer(SOMETHING_WENT_WRONG_TEMPLATE)

            if event.message is None:
                return

            return await event.message.answer(SOMETHING_WENT_WRONG_TEMPLATE)
