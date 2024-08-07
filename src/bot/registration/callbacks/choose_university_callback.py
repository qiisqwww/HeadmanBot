from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import RegistrationContext
from src.bot.common.resources import void_inline_buttons
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.registration.callback_data import UniversityCallbackData
from src.bot.registration.finite_state.registration_states import RegistrationStates
from src.bot.registration.resources.templates import (
    ASK_GROUP_TEMPLATE,
    successful_university_choose_template,
)
from src.modules.student_management.application.queries import GetUniversityByAliasQuery

__all__ = [
    "include_choose_university_router",
]


choose_university_router = Router()


def include_choose_university_router(root_router: RootRouter) -> None:
    root_router.include_router(choose_university_router)


@choose_university_router.callback_query(UniversityCallbackData.filter())
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: UniversityCallbackData,
    state: RegistrationContext,
    get_university_query: GetUniversityByAliasQuery,
) -> None:
    if callback.message is None:
        return

    chosen_uni = await get_university_query.execute(callback_data.university_alias)

    await state.set_university_alias(callback_data.university_alias)

    await safe_message_edit(
        callback,
        successful_university_choose_template(chosen_uni.name),
        reply_markup=void_inline_buttons(),
    )
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await state.set_state(RegistrationStates.waiting_group)
