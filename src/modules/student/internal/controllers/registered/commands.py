from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from src.kernel import Router
from src.modules.student.internal.resources.templates import FAQ_TEMPLATE

registered_commands_router = Router(
    throttling=True,
    inject_user=True,
)


__all__ = [
    "registered_commands_router",
]


@registered_commands_router.message(Command("faq"))
async def faq_command(message: Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_TEMPLATE)
