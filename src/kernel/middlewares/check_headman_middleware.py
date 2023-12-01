from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from loguru import logger

from src.database import get_postgres_pool
from src.kernel.protocols import PermissionsServiceProtocol

from .templates import MUST_BE_HEADMEN_TEMPLATE

HandlerType: TypeAlias = Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "CheckHeadmanMiddleware",
]


class CheckHeadmanMiddleware(BaseMiddleware):
    _must_be_headman: bool
    _service: type[PermissionsServiceProtocol]

    def __init__(self, must_be_headman: bool, service: type[PermissionsServiceProtocol]) -> None:
        self._must_be_headman = must_be_headman
        self._service = service
        super().__init__()

    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message | CallbackQuery, data: dict[str, Any]) -> Any:
        pool = await get_postgres_pool()

        async with pool.acquire() as con:
            student_service = self._service(con)
            is_headman = await student_service.check_is_headman(data["student"])

        if is_headman != self._must_be_headman and self._must_be_headman:
            await event.answer(MUST_BE_HEADMEN_TEMPLATE)
            logger.trace("headmen commands middleware finished, user must me headman to use this command")
            return

        logger.info("headman commands middleware finished")
        return await handler(event, data)
