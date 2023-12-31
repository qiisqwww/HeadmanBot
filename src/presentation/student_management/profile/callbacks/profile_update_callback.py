from aiogram.types import CallbackQuery
from loguru import logger

from src.dto.callback_data import (
    ProfileUpdateChoiceCallbackData,
    ProfileUpdateCallbackData,
    GetBackToProfileCallbackData
)
from src.dto.contexts import ProfileUpdateContext
from src.enums import Role, ProfileField
from src.dto.models import Student
from src.kernel import Router
from src.resources import (
    ASK_NEW_SURNAME_TEMPLATE,
    ASK_NEW_NAME_TEMPLATE,
    WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
    profile_update_choice_buttons,
    profile_buttons,
    profile_info,
    get_back_button
)
from src.handlers.states import ProfileUpdateStates

__all__ = [
    "profile_menu_router",
]


profile_menu_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


@profile_menu_router.callback_query(ProfileUpdateCallbackData.filter())
@logger.catch
async def profile_update(callback: CallbackQuery, state: ProfileUpdateContext) -> None:
    if callback.message is None:
        return

    await callback.message.edit_text(
        text=WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
        reply_markup=profile_update_choice_buttons()
    )

    await state.clear()


@profile_menu_router.callback_query(GetBackToProfileCallbackData.filter())
@logger.catch
async def back_to_profile(callback: CallbackQuery, student: Student) -> None:
    await callback.message.edit_text(
        text=profile_info(student.surname, student.name, student.role),
        reply_markup=profile_buttons()
    )


@profile_menu_router.callback_query(ProfileUpdateChoiceCallbackData.filter())
@logger.catch
async def profile_update_choice(
    callback: CallbackQuery,
    callback_data: ProfileUpdateChoiceCallbackData,
    state: ProfileUpdateContext
) -> None:
    if callback.message is None:
        return

    if callback_data.updating_data == ProfileField.name:
        await callback.message.edit_text(
            ASK_NEW_NAME_TEMPLATE,
            reply_markup=get_back_button()
        )
        await state.set_state(ProfileUpdateStates.waiting_new_name)

    if callback_data.updating_data == ProfileField.surname:
        await callback.message.edit_text(
            ASK_NEW_SURNAME_TEMPLATE,
            reply_markup=get_back_button()
        )
        await state.set_state(ProfileUpdateStates.waiting_new_surname)