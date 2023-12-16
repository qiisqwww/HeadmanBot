from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.resources import FAQ_TEMPLATE

help_router = Router(
    must_be_registered=True
)


__all__ = [
    "help_router",
]


@help_router.message(F.text == "Помощь")
async def faq_command(message: Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_TEMPLATE)
