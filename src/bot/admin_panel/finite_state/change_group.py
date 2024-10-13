from aiogram.types import Message

from src.bot.admin_panel.finite_state.change_group_admin_states import ChangeGroupAdminStates
from src.bot.admin_panel.resources.inline_buttons import cancel_button
from src.bot.admin_panel.resources.templates import (
    CHOSEN_GROUP_DOES_NOT_EXIST_TEMPLATE,
    YOUR_GROUP_WAS_CHANGED_TEMPLATE,
    GROUP_BELONGS_TO_ANOTHER_UNI_TEMPLATE
)
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupAdminContext
from src.common.infrastructure import DEBUG
from src.modules.student_management.application.commands.change_admin_group_command import (
    ChangeAdminGroupCommand,
    GroupWasNotRegisteredException,
    GroupBelongsToAnotherUviException
)
from src.modules.student_management.domain.enums import Role

__all__ = [
    "include_input_new_group_finite_state_router",
]

input_new_group_finite_state_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_input_new_group_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(input_new_group_finite_state_router)


@input_new_group_finite_state_router.message(ChangeGroupAdminStates.waiting_group)
async def input_new_group(
        message: Message,
        state: ChangeGroupAdminContext,
        change_admin_group_command: ChangeAdminGroupCommand,
) -> None:
    if message.text is None or message.from_user is None:
        return

    telegram_id = int(message.from_user.id)
    group_name = message.text.strip()
    university_id = await state.university_id
    try:
        await change_admin_group_command.execute(telegram_id, group_name, university_id)
    except GroupWasNotRegisteredException:
        await message.answer(CHOSEN_GROUP_DOES_NOT_EXIST_TEMPLATE, reply_markup=cancel_button())
        await state.set_state(ChangeGroupAdminStates.waiting_group)
        return
    except GroupBelongsToAnotherUviException:
        await message.answer(GROUP_BELONGS_TO_ANOTHER_UNI_TEMPLATE, reply_markup=cancel_button())
        await state.set_state(ChangeGroupAdminStates.waiting_group)
        return

    await message.answer(YOUR_GROUP_WAS_CHANGED_TEMPLATE)
    await state.clear()
