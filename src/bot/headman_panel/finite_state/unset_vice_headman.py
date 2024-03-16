from aiogram import Bot, F
from aiogram.types import Message

from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.headman_panel_states import HeadmanPanelStates
from src.bot.headman_panel.resources.inline_buttons import group_panel_menu
from src.modules.student_management.application.commands import (
    UnmakeStudentViceHeadmanCommand,
)
from src.modules.student_management.domain.enums.role import Role
from src.modules.student_management.domain.models.student import Student

unset_vice_headman_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_profile_update_router(root_router: RootRouter) -> None:
    root_router.include_router(unset_vice_headman_router)


@unset_vice_headman_router.message(
    F.text,
    HeadmanPanelStates.waiting_surname_and_name_for_unset,
)
async def unset_vice_headman(
    bot: Bot,
    message: Message,
    student: Student,
    unmake_student_vice_headman_command: UnmakeStudentViceHeadmanCommand,
) -> None:
    if message.text is None:
        return

    last_name, first_name = message.text.split()
    prev_vice_headman_id = await unmake_student_vice_headman_command.execute(
        student.group_id,
        last_name,
        first_name,
    )

    await bot.send_message(
        prev_vice_headman_id,
        "Вы были понижены",
        reply_markup=group_panel_menu(Role.STUDENT),
    )
