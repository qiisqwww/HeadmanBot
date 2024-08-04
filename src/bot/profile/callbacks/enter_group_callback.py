from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import EnterGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import EnterGroupCallbackData
from src.bot.profile.finite_state.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.inline_buttons import role_buttons
from src.bot.profile.resources.templates import CHOOSE_NEW_ROLE_TEMPLATE
from src.modules.student_management.application.commands import ClearStudentEnterGroupDataIfExistsCommand

__all__ = [
    "include_enter_group_callback_router",
]

enter_group_callback_router = Router(
    must_be_registered=True,
)


def include_enter_group_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(enter_group_callback_router)


@enter_group_callback_router.callback_query(EnterGroupCallbackData.filter())
async def enter_group(
        callback: CallbackQuery,
        state: EnterGroupContext,
        clear_student_enter_group_data_if_exists_command: ClearStudentEnterGroupDataIfExistsCommand,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await clear_student_enter_group_data_if_exists_command.execute(callback.from_user.id)

    await safe_message_edit(
        callback,
        CHOOSE_NEW_ROLE_TEMPLATE,
        reply_markup=role_buttons(),
    )
    await state.set_state(ProfileUpdateStates.waiting_new_role)
