from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import UniversityCallbackData
from src.dto.contexts import RegistrationContext
from src.handlers.finite_state.registration import RegistrationStates
from src.kernel import Router
from src.resources import (
    ASK_GROUP_TEMPLATE,
    inline_void_button,
    successful_university_choose_template,
)
from src.services import UniversityService

__all__ = ["choose_university_router"]


choose_university_router = Router(must_be_registered=False)


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
    await callback.message.delete()
    await callback.message.answer(
        successful_university_choose_template(choosen_uni.name),
        reply_markup=inline_void_button()
    )
    await callback.message.answer(ASK_GROUP_TEMPLATE)

    await registration_ctx.set_state(RegistrationStates.waiting_group)
