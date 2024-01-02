from aiogram.types import CallbackQuery

from src.application.student_management.queries import GetUniversityByAliasQuery
from src.presentation.common import Router
from src.presentation.common.resources.void_inline_buttons import inline_void_button

from ..callback_data import UniversityCallbackData
from ..registration_context import RegistrationContext
from ..registration_states import RegistrationStates
from ..resources.templates import (
    ASK_GROUP_TEMPLATE,
    successful_university_choose_template,
)

__all__ = [
    "choose_university_router",
]


choose_university_router = Router(must_be_registered=False)


@choose_university_router.callback_query(UniversityCallbackData.filter())
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: UniversityCallbackData,
    state: RegistrationContext,
    get_university_query: GetUniversityByAliasQuery,
) -> None:
    if callback.message is None:
        return

    choosen_uni = await get_university_query.execute(callback_data.university_alias)

    await state.set_university_alias(callback_data.university_alias)

    await callback.message.delete()
    await callback.message.answer(
        successful_university_choose_template(choosen_uni.name), reply_markup=inline_void_button()
    )
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await state.set_state(RegistrationStates.waiting_group)
