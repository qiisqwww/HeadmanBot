from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand

from .templates import HELP_TEMPLATE

__all__ = [
    "include_help_command_router",
]

help_command_router = Router(must_be_registered=True)


@help_command_router.message(CommandFilter(TelegramCommand.HELP))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEMPLATE)


def include_help_command_router(root_router: RootRouter) -> None:
    root_router.include_router(help_command_router)
