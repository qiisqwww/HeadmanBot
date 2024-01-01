from aiogram.types import CallbackQuery
from loguru import logger

from src.application.student_management.queries import GetAllUniversitiesQuery
from src.presentation.common.resources.void_inline_buttons import inline_void_button
from src.presentation.common.router import Router

from ..callback_data import ChooseRoleCallbackData
from ..registration_context import RegistrationContext
from ..registration_states import RegistrationStates
from ..resources.inline_buttons import university_list_buttons
from ..resources.templates import (
    ASK_UNIVERSITY_TEMPLATE,
    successful_role_choose_template,
)

__all__ = [
    "choose_role_router",
]

choose_role_router = Router(
    must_be_registered=False,
)


@choose_role_router.callback_query(ChooseRoleCallbackData.filter())
@logger.catch
async def get_role_from_user(
    callback: CallbackQuery,
    callback_data: ChooseRoleCallbackData,
    state: RegistrationContext,
    get_all_universities_query: GetAllUniversitiesQuery,
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await state.set_role(callback_data.role)

    await callback.message.answer(successful_role_choose_template(await state.role), reply_markup=inline_void_button())

    universities = await get_all_universities_query.execute()

    await callback.message.delete()
    await callback.message.answer(ASK_UNIVERSITY_TEMPLATE, reply_markup=university_list_buttons(universities))

    await state.set_state(RegistrationStates.waiting_university)
