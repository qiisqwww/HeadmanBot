from datetime import datetime, timedelta, timezone
from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import CallbackQuery, TelegramObject
from loguru import logger

from src.services import LessonService
from src.external.database import get_postgres_pool
from src.dto import Student

__all__ = [
    "CallbackMiddleware",
]


HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]


class CallbackMiddleware(BaseMiddleware):
    @logger.catch
    async def __call__(self, handler: HandlerType, event: CallbackQuery, data: dict[str, Any]) -> Any:
        logger.info("callback middleware started")

        if event.message is None:
            return

        logger.info(f"EVENT TYPE={type(event)}")

        flag = get_flag(data, "callback")
        student: Student = data["student"]

        if flag == "poll":
            lesson_len = timedelta(hours=1, minutes=30)
            now = datetime.now(tz=timezone.utc)

            pool = await get_postgres_pool()
            async with pool.acquire() as con:
                lesson_service = LessonService()
                today_lessons = await lesson_service.filter_by_student_id(student)

            first_lesson_time = datetime.combine(datetime.today(), today_lessons[0].start_time)

            if now > first_lesson_time + lesson_len:
                logger.info("(poll) callback middleware finished, lesson was already started")
                await event.message.edit_text("Вы не можете отметиться! Занятия уже начались!")
                return

        logger.info(f"({flag}) callback middleware finished")
        return await handler(event, data)
