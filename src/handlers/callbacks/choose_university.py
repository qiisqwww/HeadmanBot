from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from loguru import logger

from src.kernel import Router
from src.callback_data import UniversityCallbackData
from src.resources import (
    ASK_UNIVERSITY_TEMPLATE,
    ASK_GROUP_TEMPLATE,
    successful_university_choose_template,
    inline_void_button
)
from src.handlers.finite_state.registration import (
    RegistrationStates,
)
from src.registration_context import RegistrationContext
from src.services import UniversityService


__all__ = [
    "choose_university_router"
]


choose_university_router = Router()


@choose_university_router.callback_query(UniversityCallbackData.filter())
@logger.catch
async def get_university_from_user(
    callback: CallbackQuery,
    callback_data: UniversityCallbackData,
    state: FSMContext,
    university_service: UniversityService,
) -> None:
    registration_ctx = RegistrationContext(state)

    if callback.message is None:
        return

    choosen_uni = await university_service.get_by_alias(callback_data.university_alias)

    await registration_ctx.set_university_alias(callback_data.university_alias)

    await callback.message.edit_text(ASK_UNIVERSITY_TEMPLATE, reply_markup=inline_void_button())
    await callback.message.answer(successful_university_choose_template(choosen_uni.name))
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
