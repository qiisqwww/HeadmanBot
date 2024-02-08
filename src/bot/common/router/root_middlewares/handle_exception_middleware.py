from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from src.modules.common.infrastructure.config.config import ADMIN_IDS

from .templates import SOMETHING_WENT_WRONG_TEMPLATE, something_went_wrong_template

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
            for admin_id in ADMIN_IDS:
                await event.bot.send_message(admin_id, something_went_wrong_template(e, event.from_user.id))

            return await event.answer(SOMETHING_WENT_WRONG_TEMPLATE, show_alert=True)
