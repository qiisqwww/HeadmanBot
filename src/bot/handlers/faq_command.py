from aiogram import Router, types
from aiogram.filters import Command
from loguru import logger

from src.buttons import default_buttons
from src.messages import FAQ_MESSAGE
from src.middlewares import CheckRegistrationMiddleware

__all__ = [
    "faq_router",
]

faq_router = Router()
faq_router.message.middleware(CheckRegistrationMiddleware(must_be_registered=True))


@faq_router.message(Command("faq"))
async def faq_command(message: types.Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_MESSAGE, reply_markup=default_buttons(is_headman=True))
