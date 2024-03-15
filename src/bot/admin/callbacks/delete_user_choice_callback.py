from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.admin.callback_data import (
    DeleteByTGIDCallbackData,
    DeleteByNameAndGroupCallbackData
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
async def get_groups_list(
    callback: CallbackQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return


@delete_user_choice_router.callback_query(DeleteByNameAndGroupCallbackData.filter())
async def get_groups_list(
        callback: CallbackQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return


    

