from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.common.resources.void_inline_buttons import void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "CheckMessageExpireMiddleware",
]


class CheckMessageExpireMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: HandlerType,
        event: EventType,
        data: dict[str, Any],
    ) -> Any:
        if data.get("callback_data") is None:
            return await handler(event, data)

        if not hasattr(data["callback_data"], "created_at"):
            return await handler(event, data)

        if (
            isinstance(event, CallbackQuery)
            and data["callback_data"].created_at != datetime.today().date()
        ):
            if event.message is not None:
                await safe_message_edit(
                    event,
                    "Сообщение устарело",
                    reply_markup=void_inline_buttons(),
                )
            return None

        return await handler(event, data)
