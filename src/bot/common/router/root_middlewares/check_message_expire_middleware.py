from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.bot.common.resources.void_inline_buttons import void_inline_buttons

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

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
        if data.get("callback_data", None) is None:
            return await handler(event, data)

        if not hasattr(data["callback_data"], "created_at"):
            return await handler(event, data)

        if data["callback_data"].created_at != datetime.today().date():
            await event.message.edit_text(
                "Сообщение устарело",
                reply_markup=void_inline_buttons(),
            )
            return None

        return await handler(event, data)
