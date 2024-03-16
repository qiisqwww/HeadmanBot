from aiogram import Bot, F
from aiogram.types import Message

from src.bot.common.router import RootRouter, Router
from src.bot.headman_panel.headman_panel_states import HeadmanPanelStates
from src.bot.headman_panel.resources.inline_buttons import group_panel_menu
from src.modules.student_management.application.commands.make_student_viceheadman_command import (
    MakeStudentViceHeadmanCommand,
)
from src.modules.student_management.domain.enums.role import Role
from src.modules.student_management.domain.models.student import Student

set_vice_headman_router = Router(
    must_be_registered=True,
    minimum_role=Role.HEADMAN,
)


def include_profile_update_router(root_router: RootRouter) -> None:
    root_router.include_router(set_vice_headman_router)


@set_vice_headman_router.message(
    F.text,
    HeadmanPanelStates.waiting_surname_and_name_for_set,
)
async def set_vice_headman(
    bot: Bot,
    message: Message,
    student: Student,
    make_student_vice_headman_command: MakeStudentViceHeadmanCommand,
) -> None:
    if message.text is None:
        return

    last_name, first_name = message.text.split()

    new_vice_headman_id = await make_student_vice_headman_command.execute(
        student.group_id,
        last_name,
        first_name,
    )

    await bot.send_message(
        new_vice_headman_id,
        "Вы были повышены",
        reply_markup=group_panel_menu(Role.VICE_HEADMAN),
    )
