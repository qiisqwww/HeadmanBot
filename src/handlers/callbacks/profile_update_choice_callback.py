from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import ProfileUpdateCallbackData
from src.dto.contexts import ProfileUpdateContext
from src.enums import Role, ProfileField
from src.kernel import Router
from src.resources import (
    ASK_NEW_SURNAME_TEMPLATE,
    ASK_NEW_NAME_TEMPLATE
)
from src.handlers.states import ProfileUpdateStates

__all__ = [
    "profile_update_choice_callback_router",
]


profile_update_choice_callback_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@profile_update_choice_callback_router.callback_query(ProfileUpdateCallbackData.filter())
@logger.catch
async def profile_update_choice(
    callback: CallbackQuery,
    callback_data: ProfileUpdateCallbackData,
    state: ProfileUpdateContext
):
    if callback.message is None:
        return

    if callback_data.updating_data == ProfileField.name:
        await callback.message.answer(ASK_NEW_NAME_TEMPLATE)
        await state.set_state(ProfileUpdateStates.waiting_new_name)

    if callback_data.updating_data == ProfileField.surname:
        await callback.message.answer(ASK_NEW_SURNAME_TEMPLATE)
        await state.set_state(ProfileUpdateStates.waiting_new_surname)
