from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import EnterGroupContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import ChooseUniCallbackData
from src.bot.profile.finite_state.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.templates import (
    INPUT_GROUP_NAME_TEMPLATE,
    successful_university_choose_template,
)
from src.modules.student_management.application.queries import GetUniversityByAliasQuery

__all__ = [
    "include_choose_new_university_router",
]


choose_new_university_router = Router(
    must_be_registered=True,
)


def include_choose_new_university_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_new_university_router)


@choose_new_university_router.callback_query(ChooseUniCallbackData.filter())
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: ChooseUniCallbackData,
    state: EnterGroupContext,
    get_university_query: GetUniversityByAliasQuery,
) -> None:
    if callback.message is None:
        return

    chosen_uni = await get_university_query.execute(callback_data.university_alias)
    await state.set_university_alias(university_alias=callback_data.university_alias)

    await safe_message_edit(
        callback,
        successful_university_choose_template(chosen_uni.name),
    )
    await callback.message.answer(INPUT_GROUP_NAME_TEMPLATE)

    await state.set_state(ProfileUpdateStates.waiting_new_group)
