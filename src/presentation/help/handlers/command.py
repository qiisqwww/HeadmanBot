from aiogram.types import Message

from ...common.command_filter import CommandFilter, TelegramCommand
from ...common.router import Router
from ..resources import HELP_TEMPLATE

help_command_router = Router(
    must_be_registered=True,
)


__all__ = [
    "help_command_router",
]


@help_command_router.message(CommandFilter(TelegramCommand.HELP))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEMPLATE)
