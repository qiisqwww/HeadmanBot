from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.change_group.resources.templates import CHANGE_OR_QUIT_TEMPLATE
from src.bot.change_group.resources.inline_buttons import change_group_buttons

__all__ = [
    "include_change_group_command_router",
]


change_group_command_router = Router(
    must_be_registered=True,
)


def include_change_group_command_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_command_router)


@change_group_command_router.message(CommandFilter(TelegramCommand.CHANGE_GROUP))
async def profile_command(message: Message) -> None:
    await message.answer(CHANGE_OR_QUIT_TEMPLATE, reply_markup=change_group_buttons())
