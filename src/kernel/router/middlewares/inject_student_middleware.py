from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.services import StudentService

from .templates import ALREADY_REGISTERED_TEMPLATE, MUST_BE_REG_TEMPLATE

__all__ = [
    "InjectStudentMiddleware",
]

HandlerType: TypeAlias = Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]


class InjectStudentMiddleware(BaseMiddleware):
    _must_be_registered: bool

    def __init__(self, must_be_registered: bool) -> None:
        self._must_be_registered = must_be_registered
        super().__init__()

    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message | CallbackQuery, data: dict[str, Any]) -> Any:
        logger.trace("Check is user registred middleware started.")

        if event.from_user is None:
            return

        if data.get("student", None) is None:
            student_service = StudentService(data["postgres_con"])
            student = await student_service.find_student(event.from_user.id)
        else:
            student = data["student"]

        is_registered = student is not None

        if is_registered != self._must_be_registered and not self._must_be_registered:
            await event.answer(ALREADY_REGISTERED_TEMPLATE)
            logger.trace("middleware finished, already registered")
            return

        if is_registered != self._must_be_registered and self._must_be_registered:
            await event.answer(MUST_BE_REG_TEMPLATE)
            logger.trace("middleware finished, must be registered")
            return

        logger.trace("Check is user registred middleware finished.")
        data["student"] = student

        return await handler(event, data)
