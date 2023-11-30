from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from src.modules.student.resources.templates import FAQ_TEMPLATE

registered_commands_router = Router()
registered_commands_router.message.middleware(Check(must_be_registered=True))


__all__ = [
    "registered_commands_router",
]


@registered_commands_router.message(Command("faq"))
async def faq_command(message: Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_TEMPLATE, reply_markup=default_buttons(is_headman=True))
