from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupContext
from src.bot.change_group.finite_state.change_group_states import ChangeGroupStates
from src.bot.change_group.resources.templates import (
    GROUP_DOESNT_REGISTERED_TEMPLATE,
    HEADMAN_ALREADY_EXISTS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE,
    YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE,
    successful_role_choose_template
)
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.change_group.resources.inline_buttons import get_back_button
from src.bot.change_group.callback_data import ChooseRoleCallbackData
from src.modules.student_management.application.queries import (
    FindGroupByNameAndAliasQuery,
    FindGroupHeadmanQuery,
)
from src.modules.student_management.domain import Role

__all__ = [
    "include_choose_role_callback_router"
]


choose_role_callback_router = Router(
    must_be_registered=True
)


def include_choose_role_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_role_callback_router)


@choose_role_callback_router.callback_query(ChooseRoleCallbackData.filter())
async def new_role_handler(
        callback: CallbackQuery,
        callback_data: ChooseRoleCallbackData,
        state: ChangeGroupContext,
        find_group_headman_query: FindGroupHeadmanQuery,
        find_group_by_name_and_alias_query: FindGroupByNameAndAliasQuery,
) -> None:
    await safe_message_edit(
        callback,
        successful_role_choose_template(callback_data.role)
    )

    if callback_data.role == Role.STUDENT and await state.new_group_name is None:
        await callback.message.answer(GROUP_DOESNT_REGISTERED_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ChangeGroupStates.waiting_new_group)
        return

    group = await find_group_by_name_and_alias_query.execute(
        await state.new_group_name,
        await state.university_alias,
    )

    if state.new_group_name is not None and callback_data.role == Role.HEADMAN:
        group_headman = await find_group_headman_query.execute(group.id)
        if group_headman is not None:
            await callback.message.answer(HEADMAN_ALREADY_EXISTS_TEMPLATE, reply_markup=get_back_button())
            await state.set_state(ChangeGroupStates.waiting_new_group)
            return

    match callback_data.role:
        case Role.STUDENT:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_HEADMAN_TEMPLATE)
        case Role.HEADMAN:
            await callback.message.answer(YOUR_APPLY_WAS_SENT_TO_ADMINS_TEMPLATE)

    # TODO

    await state.clear()
    await state.set_state(ChangeGroupStates.on_verification)
