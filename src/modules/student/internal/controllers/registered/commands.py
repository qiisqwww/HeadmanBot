from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from src.kernel.middlewares import InjectStudentMiddleware
from src.modules.student.api.contracts import PermissionsServiceContract
from src.modules.student.internal.resources.templates import FAQ_TEMPLATE

registered_commands_router = Router()
registered_commands_router.message.middleware(
    InjectStudentMiddleware(must_be_registered=True, service=PermissionsServiceContract)
)


__all__ = [
    "registered_commands_router",
]


@registered_commands_router.message(Command("faq"))
async def faq_command(message: Message) -> None:
    logger.trace("faq command")

    await message.answer(text=FAQ_TEMPLATE)
