from datetime import datetime, timedelta, timezone
from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from loguru import logger

from src.database import get_pool
from src.services import StudentService

__all__ = [
    "CallbackMiddleware",
]


HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]


class CallbackMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        logger.info("callback middleware started")

        if event.from_user is None:
            return

        user_id = event.from_user.id
        flag = get_flag(data, "callback")

        if flag == "poll":
            lesson_len = timedelta(hours=1, minutes=30)
            now = datetime.now(tz=timezone.utc)

            pool = await get_pool()
            async with pool.acquire() as con:
                student_service = StudentService(con)
                schedule = await student_service.get_schedule(user_id)

            first_lesson_time = datetime.combine(datetime.today(), schedule[0].start_time)

            if now > first_lesson_time + lesson_len:
                logger.info("(poll) callback middleware finished, lesson was already started")
                await event.message.edit_text("Вы не можете отметиться! Занятия уже начались!")
                return

        logger.info(f"({flag}) callback middleware finished")
        return await handler(event, data)
