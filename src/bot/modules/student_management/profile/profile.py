from aiogram import F
from aiogram.types import Message
from loguru import logger

from src.enums import TelegramCommand, Role
from src.kernel import Router
from src.resources import (
    profile_info,
    profile_buttons
)
from src.dto.models import Student

__all__ = [
    "profile_router",
]


profile_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@profile_router.message(F.text == TelegramCommand.PROFILE)
@logger.catch
async def profile_command(message: Message, student: Student) -> None:
    await message.answer(
        text=profile_info(student.surname, student.name, student.role),
        reply_markup=profile_buttons()
    )
