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
from src.modules.student_management.domain.enums import Role
from src.modules.common.infrastructure import DEBUG
from src.modules.student_management.application.queries import GetStudentsCountQuery
from src.modules.edu_info.application.queries import GetAllGroupsQuery

__all__ = [
    "include_admin_panel_options_router",
]

admin_panel_options_router = Router(
    must_be_registered=True,
    minimum_role=Role.ADMIN if not DEBUG else Role.STUDENT
)


def include_admin_panel_options_router(root_router: RootRouter) -> None:
    root_router.include_router(admin_panel_options_router)


@admin_panel_options_router.callback_query(UsersCountCallbackData.filter())
async def get_users_count(
    callback: CallbackQuery,
    get_students_count_query: GetStudentsCountQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    users_count = await get_students_count_query.execute()

    await callback.message.answer(users_count_template(users_count))
    await callback.answer(None)


@admin_panel_options_router.callback_query(GroupsListCallbackData.filter())
async def get_groups_list(
    callback: CallbackQuery,
    get_all_groups_query: GetAllGroupsQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    groups = await get_all_groups_query.execute()

    await callback.message.answer(group_list_template(groups))
    await callback.answer(None)


@admin_panel_options_router.callback_query(MakeNewAdminCallbackData.filter())  # InDev
async def made_user_admin(
    callback: CallbackQuery
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await callback.answer(None)

    return
