from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.bot.common.resources import SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE

if TYPE_CHECKING:
    from src.modules.common.application.bot_notifier import BotNotifier

type EventType = Message | CallbackQuery
type HandlerType = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "HandleExceptionMiddleware",
]


class HandleExceptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: HandlerType,
        event: EventType,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.exception(e)
            notifier: BotNotifier = data["notifier"]
            await notifier.notify_about_exception(e, event.from_user)

            return await event.answer(
                SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE,
                show_alert=True,
            )
