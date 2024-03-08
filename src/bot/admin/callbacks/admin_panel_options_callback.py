from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.admin.callback_data import (
    UsersCountCallbackData,
    GroupsListCallbackData,
    MakeNewAdminCallbackData,
)
from src.bot.admin.resources.templates import (
    users_count_template,
    group_list_template
)
from src.modules.student_management.application.queries import GetStudentsCountQuery

__all__ = [
    "include_admin_panel_options_router",
]

admin_panel_options_router = Router(
    must_be_registered=True
)


def include_admin_panel_options_router(root_router: RootRouter) -> None:
    root_router.include_router(admin_panel_options_router)


@admin_panel_options_router.callback_query(UsersCountCallbackData.filter())
async def get_role_from_user(
    callback: CallbackQuery,
    get_students_count_query: GetStudentsCountQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    users_count = await get_students_count_query.execute()

    await callback.message.answer(users_count_template(users_count))


@admin_panel_options_router.callback_query(GroupsListCallbackData.filter())
async def get_role_from_user(
    callback: CallbackQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.message.answer(group_list_template())  # here will be a logic of getting group list


@admin_panel_options_router.callback_query(MakeNewAdminCallbackData.filter())  # InDev
async def get_role_from_user(
    callback: CallbackQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    return
