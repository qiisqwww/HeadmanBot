from aiogram.types import CallbackQuery
from loguru import logger

from src.callback_data import ChooseRoleCallbackData
from src.handlers.finite_state.registration.registration_context import RegistrationContext
from src.handlers.finite_state.registration import RegistrationStates
from src.kernel import Router
from src.resources import university_list_buttons
from src.resources import inline_void_button
from src.resources import (
    ASK_UNIVERSITY_TEMPLATE,
    CHOOSE_STUDENT_ROLE_TEMPLATE,
    successful_role_choose_template,
)
from src.services import UniversityService

__all__ = [
    "choose_role_router",
]

choose_role_router = Router()


@choose_role_router.callback_query(ChooseRoleCallbackData.filter())
@logger.catch
async def get_role_from_user(
    callback: CallbackQuery,
    callback_data: ChooseRoleCallbackData,
    state: RegistrationContext,
    university_service: UniversityService,
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await state.set_role(callback_data.role)

    await callback.message.edit_text(CHOOSE_STUDENT_ROLE_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(successful_role_choose_template(await state.role))

    universities = await university_service.all()

    await callback.message.answer(text=ASK_UNIVERSITY_TEMPLATE, reply_markup=university_list_buttons(universities))
    await state.set_state(RegistrationStates.waiting_university)
