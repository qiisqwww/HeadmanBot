from aiogram.types import CallbackQuery

from src.bot.profile.callback_data import (
    GetBackToProfileCallbackData,
    ProfileUpdateCallbackData,
    ProfileUpdateChoiceCallbackData,
)
from src.bot.common.contextes import ProfileUpdateContext
from src.modules.student_management.domain.models import Student
from src.modules.student_management.domain.enums import ProfileField, Role
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.bot.profile.profile_update_states import ProfileUpdateStates
from src.bot.common import RootRouter, Router
from src.bot.profile.resources.templates import (
    ASK_NEW_NAME_TEMPLATE,
    ASK_NEW_SURNAME_TEMPLATE,
    WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
    profile_info,
)
from src.bot.profile.resources.inline_buttons import (
    get_back_button,
    profile_buttons,
    profile_update_choice_buttons
)

__all__ = [
    "include_profile_menu_router",
]


profile_menu_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
    )


def include_profile_menu_router(root_router: RootRouter) -> None:
    root_router.include_router(profile_menu_router)


@profile_menu_router.callback_query(ProfileUpdateCallbackData.filter())
async def profile_update(callback: CallbackQuery, state: ProfileUpdateContext) -> None:
    if callback.message is None:
        return

    await callback.message.edit_text(
        text=WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
        reply_markup=profile_update_choice_buttons()
    )

    await state.clear()


@profile_menu_router.callback_query(GetBackToProfileCallbackData.filter())
async def back_to_profile(
        callback: CallbackQuery,
        student: Student,
        get_edu_profile_info_query: GetEduProfileInfoQuery
) -> None:
    edu_info = await get_edu_profile_info_query.execute(student.group_id)

    await callback.message.edit_text(
        text=profile_info(student, edu_info),
        reply_markup=profile_buttons(),
    )


@profile_menu_router.callback_query(ProfileUpdateChoiceCallbackData.filter())
async def profile_update_choice(
    callback: CallbackQuery,
    callback_data: ProfileUpdateChoiceCallbackData,
    state: ProfileUpdateContext,
) -> None:
    if callback.message is None:
        return

    if callback_data.updating_data == ProfileField.NAME:
        await callback.message.edit_text(ASK_NEW_NAME_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ProfileUpdateStates.waiting_new_name)

    if callback_data.updating_data == ProfileField.SURNAME:
        await callback.message.edit_text(ASK_NEW_SURNAME_TEMPLATE, reply_markup=get_back_button())
        await state.set_state(ProfileUpdateStates.waiting_new_surname)
