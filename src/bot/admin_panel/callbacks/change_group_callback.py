from aiogram.types import CallbackQuery

from src.bot.admin_panel.callback_data import ChangeGroupCallbackData
from src.bot.admin_panel.resources.templates import CHOOSE_UNI_TEMPLATE
from src.bot.admin_panel.resources.inline_buttons import cancel_button
from src.bot.admin_panel.finite_state.change_group_admin_states import ChangeGroupAdminStates
from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupAdminContext
from src.modules.common.infrastructure import DEBUG
from src.modules.student_management.domain.enums import Role

__all__ = [
    "include_change_group_router",
]

change_group_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT,
)


def include_change_group_router(root_router: RootRouter) -> None:
    root_router.include_router(change_group_router)


@change_group_router.callback_query(ChangeGroupCallbackData.filter())
async def change_group(callback: CallbackQuery, state: ChangeGroupAdminContext) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(CHOOSE_UNI_TEMPLATE, reply_markup=cancel_button())
    await callback.answer(None)

    await state.set_state(ChangeGroupAdminStates.waiting_university)
