from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ChangeGroupAdminContext
from src.bot.common.resources import void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.admin_panel.callback_data import ChooseUniCallbackData
from src.bot.admin_panel.finite_state.change_group_admin_states import ChangeGroupAdminStates
from src.bot.admin_panel.resources.templates import (
    INPUT_NEW_GROUP_NAME_TEMPLATE,
    successful_university_choose_template
)
from src.modules.student_management.application.queries import GetUniversityByAliasQuery

__all__ = [
    "include_chosen_uni_callback_router",
]


chosen_uni_callback_router = Router()


def include_chosen_uni_callback_router(root_router: RootRouter) -> None:
    root_router.include_router(chosen_uni_callback_router)


@chosen_uni_callback_router.callback_query(ChooseUniCallbackData.filter())
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: ChooseUniCallbackData,
    state: ChangeGroupAdminContext,
    get_university_query: GetUniversityByAliasQuery,
) -> None:
    if callback.message is None:
        return

    chosen_uni = await get_university_query.execute(callback_data.university_alias)

    await state.set_university_id(chosen_uni.id)

    await safe_message_edit(
        callback,
        successful_university_choose_template(chosen_uni.name),
        reply_markup=void_inline_buttons(),
    )
    await callback.message.answer(INPUT_NEW_GROUP_NAME_TEMPLATE)

    await state.set_state(ChangeGroupAdminStates.waiting_group)
