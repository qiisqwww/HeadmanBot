from aiogram.types import Message

from ...common.command_filter import CommandFilter, TelegramCommand
from ...common.router import Router
from .templates import HELP_TEMPLATE

help_command_router = Router(
    must_be_registered=True,
)


__all__ = [
    "include_help_command_router",
]


@help_command_router.message(CommandFilter(TelegramCommand.HELP))
async def help_command(message: Message) -> None:
    await message.answer(HELP_TEMPLATE)


def include_help_command_router(root_router: Router) -> None:
    root_router.include_router(help_command_router)
