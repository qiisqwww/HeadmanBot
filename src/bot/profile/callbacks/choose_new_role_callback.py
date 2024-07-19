from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import EnterGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import ChooseNewRoleCallbackData
from src.bot.profile.finite_state.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.templates import (
    INPUT_YOUR_UNIVERSITY_TEMPLATE,
    successful_role_choose_template
)
from src.bot.profile.resources.inline_buttons import university_list_buttons
from src.modules.student_management.application.queries import GetAllUniversitiesQuery

__all__ = [
    "include_choose_new_role_router",
]

choose_new_role_router = Router(
    must_be_registered=True
)


def include_choose_new_role_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_new_role_router)


@choose_new_role_router.callback_query(ChooseNewRoleCallbackData.filter())
async def get_role_from_user(
    callback: CallbackQuery,
    callback_data: ChooseNewRoleCallbackData,
    state: EnterGroupContext,
    get_all_universities_query: GetAllUniversitiesQuery,
) -> None:
    if callback.message is None or callback.message.from_user is None:
        return

    await state.set_role(callback_data.role)

    await safe_message_edit(
        callback,
        successful_role_choose_template(await state.role)
    )

    universities = await get_all_universities_query.execute()

    await callback.message.answer(
        INPUT_YOUR_UNIVERSITY_TEMPLATE,
        reply_markup=university_list_buttons(universities)
    )

    await state.set_state(ProfileUpdateStates.waiting_new_uni)


