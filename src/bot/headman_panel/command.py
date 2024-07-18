from aiogram.types import Message

from src.bot.common import CommandFilter, RootRouter, Router, TelegramCommand
from src.bot.headman_panel.resources.inline_buttons import group_panel_menu
from src.modules.student_management.domain import Role, Student

__all__ = [
    "include_group_panel_command_router",
]


group_panel_command_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


def include_group_panel_command_router(root_router: RootRouter) -> None:
    root_router.include_router(group_panel_command_router)


@group_panel_command_router.message(CommandFilter(TelegramCommand.GROUP_PANEL))
async def start_group_panel(
    message: Message,
    student: Student,
) -> None:
    await message.answer(
        "Выберите действие:",
        reply_markup=group_panel_menu(student.role),
    )
