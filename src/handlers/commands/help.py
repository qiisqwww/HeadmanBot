from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.resources import FAQ_TEMPLATE

registered_commands_router = Router(
    must_be_registered=True
)


__all__ = [
    "registered_commands_router",
]


@registered_commands_router.message(F.text == "Помощь")
async def faq_command(message: Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_TEMPLATE)
