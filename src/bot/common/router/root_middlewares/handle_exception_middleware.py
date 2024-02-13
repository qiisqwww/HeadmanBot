from collections.abc import Awaitable, Callable
from typing import Any, TypeAlias

from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Message, User

from src.bot.common.inform_admins_about_exception import inform_admins_about_exception
from src.bot.common.resources import SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE

EventType: TypeAlias = Message | CallbackQuery
HandlerType: TypeAlias = Callable[[EventType, dict[str, Any]], Awaitable[Any]]

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
        async def _inform_admins_about_exception_wrapper(
            exception: Exception,
            user: User | None,
        ) -> None:
            bot: Bot = data["bot"]
            await inform_admins_about_exception(bot, exception, user)

        data["inform_admins_about_exception"] = _inform_admins_about_exception_wrapper

        try:
            return await handler(event, data)
        except Exception as e:
            await _inform_admins_about_exception_wrapper(e, event.from_user)
            return await event.answer(
                SOMETHING_WENT_WRONG_FOR_STUDENT_TEMPLATE,
                show_alert=True,
            )
