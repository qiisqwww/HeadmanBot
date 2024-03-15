from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import DeleteUserContext
from src.bot.admin.delete_user_states import DeleteUserStates
from src.bot.admin.callback_data import (
    DeleteByTGIDCallbackData,
    DeleteByNameAndGroupCallbackData
)
from src.bot.admin.resources.templates import (
    INPUT_USER_TG_ID_TEMPLATE,
    INPUT_FULLNAME_GROUP_TEMPLATE
)
from src.modules.student_management.domain.enums import Role
from src.modules.common.infrastructure import DEBUG


__all__ = [
    "include_delete_user_choice_router",
]

delete_user_choice_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT
)


def include_delete_user_choice_router(root_router: RootRouter) -> None:
    root_router.include_router(delete_user_choice_router)


@delete_user_choice_router.callback_query(DeleteByTGIDCallbackData.filter())
async def ask_user_telegram_id(
        callback: CallbackQuery,
        state: DeleteUserContext
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(INPUT_USER_TG_ID_TEMPLATE)
    await state.set_state(DeleteUserStates.waiting_telegram_id)

    await callback.answer(None)


@delete_user_choice_router.callback_query(DeleteByNameAndGroupCallbackData.filter())
async def ask_user_fullname_group_name(
        callback: CallbackQuery,
        state: DeleteUserContext
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(INPUT_FULLNAME_GROUP_TEMPLATE)
    await state.set_state(DeleteUserStates.waiting_fullname_group)

    await callback.answer(None)
