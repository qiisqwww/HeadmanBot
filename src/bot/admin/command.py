from aiogram.types import Message

from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.common.router import RootRouter, Router
from .resources.templates import ADMIN_PANEL_TEMPLATE
from .resources.inline_buttons import admin_panel_buttons


__all__ = [
    "include_admin_panel_command_router",
]

admin_panel_command_router = Router()


@admin_panel_command_router.message(CommandFilter(TelegramCommand.ADMIN))
async def admin_panel_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        text=ADMIN_PANEL_TEMPLATE,
        reply_markup=admin_panel_buttons()
    )


def include_admin_panel_command_router(root_router: RootRouter) -> None:
    root_router.include_router(admin_panel_command_router)
