from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from src.bot.services import StudentService
from src.database import get_pool
from src.dto import Student

from .templates import MUST_BE_HEADMEN_TEMPLATE

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "CheckHeadmanMiddleware",
]


class CheckHeadmanMiddleware(BaseMiddleware):
    _must_be_headman: bool

    def __init__(self, must_be_headman: bool) -> None:
        self._must_be_headman = must_be_headman
        super().__init__()

    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        student: Student = data["student"]
        pool = await get_pool()

        async with pool.acquire() as con:
            student_service = StudentService(con)
            is_headman = await student_service.is_headman(student)

        if is_headman != self._must_be_headman and self._must_be_headman:
            await event.reply(MUST_BE_HEADMEN_TEMPLATE)
            logger.trace("headmen commands middleware finished, user must me headman to use this command")
            return

        logger.info("headman commands middleware finished")
        return await handler(event, data)
