import logging
from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message

from src.services.student_service import StudentService

__all__ = [
    "CallbackMiddleware",
]


class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], event: Message, data: dict[str, Any]
    ) -> Any:
        logging.info("callback middleware started")

        user_id = event.from_user.id
        flag = get_flag(data, "callback")

        if flag == "poll":
            lesson_len = timedelta(hours=1, minutes=30)
            now = datetime.now()

            async with StudentService() as student_service:
                schedule = await student_service.get_schedule(user_id)
                first_lesson_time = datetime.combine(datetime.today(), schedule[0].start_time)

                if now > first_lesson_time + lesson_len:
                    logging.warning("(poll) callback middleware finished, lesson was already started")
                    await event.message.edit_text("Вы не можете отметиться! Занятия уже начались!")
                    return

        logging.info(f"({flag}) callback middleware finished")
        return await handler(event, data)
