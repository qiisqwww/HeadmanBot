from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteUserContext
from src.bot.admin.delete_user_states import DeleteUserStates
from src.bot.admin.resources.templates import USER_WAS_DELETED_TEMPLATE
from src.modules.student_management.application.commands import (
    DeleteUserByTGIDCommand
)
from src.modules.student_management.domain.enums import Role
from src.modules.common.infrastructure import DEBUG

__all__ = [
    "include_delete_user_finite_state_router",
]

delete_user_finite_state_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT
)


def include_delete_user_finite_state_router(root_router: RootRouter) -> None:
    root_router.include_router(delete_user_finite_state_router)


@delete_user_finite_state_router.message(DeleteUserStates.waiting_telegram_id)
async def ask_user_telegram_id(
        callback: CallbackQuery,
        delete_user_by_tg_id_command: DeleteUserByTGIDCommand,
        state: DeleteUserContext,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await delete_user_by_tg_id_command.execute(int(callback.message.text))  # NEED TO CHECK WHETHER USER EXISTS !!!!
    await callback.message.answer(USER_WAS_DELETED_TEMPLATE)

    await state.clear()
    await callback.answer(None)


@delete_user_finite_state_router.message(DeleteUserStates.waiting_fullname_group)
async def ask_user_fullname_group_name(
        callback: CallbackQuery,
        state: DeleteUserContext
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return



    await state.clear()
    await callback.answer(None)
