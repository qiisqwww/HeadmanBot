from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.common.resources.main_menu import main_menu
from src.modules.student_management.domain.models.student import Student

from .templates import HELP_TEMPLATE

__all__ = [
    "include_help_command_router",
]

help_command_router = Router(must_be_registered=True)


@help_command_router.message(CommandFilter(TelegramCommand.HELP))
async def help_command(message: Message, student: Student) -> None:
    await message.answer(HELP_TEMPLATE, reply_markup=main_menu(student.role))


def include_help_command_router(root_router: RootRouter) -> None:
    root_router.include_router(help_command_router)
