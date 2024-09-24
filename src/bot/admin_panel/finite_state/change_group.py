from aiogram.types import Message

from src.bot.admin_panel.finite_state.change_group_admin_states import ChangeGroupAdminStates
from src.bot.admin_panel.resources.templates import (
    GROUP_DOES_NOT_EXIST_TEMPLATE,
    YOUR_GROUP_WAS_CHANGED_TEMPLATE
)
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupAdminContext
from src.modules.common.infrastructure import DEBUG
from src.modules.student_management.domain.enums import Role
from src.modules.edu_info.application.queries import FetchGroupByGroupName
from src.modules.student_management.application.commands import ChangeAdminGroupCommand

__all__ = [
    "include_change_group_finite_state_router",
]

change_group_finite_state_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_change_group_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_finite_state_router)


@change_group_finite_state_router.message(ChangeGroupAdminStates.waiting_group)
async def change_group_for_admin(
    message: Message,
    state: ChangeGroupAdminContext,
    fetch_group_by_group_name: FetchGroupByGroupName,
    change_admin_group_command: ChangeAdminGroupCommand,
) -> None:
    if message.text is None or message.from_user is None:
        return

    group_name = message.text.strip()
    group = await fetch_group_by_group_name.execute(group_name)

    if group is None or group.id != (await state.university_id):
        await message.answer(GROUP_DOES_NOT_EXIST_TEMPLATE)
        await state.set_state(ChangeGroupAdminStates.waiting_group)
        return

    await change_admin_group_command.execute(int(message.from_user.id), group.id)

    await message.answer(YOUR_GROUP_WAS_CHANGED_TEMPLATE)
    await state.clear()
