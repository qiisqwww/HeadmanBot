from aiogram.types import CallbackQuery

from src.bot.common import RootRouter, Router
from src.bot.common.contextes import ProfileUpdateContext
from src.bot.common.safe_message_edit import safe_message_edit
from src.bot.profile.callback_data import (
    GetBackToProfileCallbackData,
    ProfileUpdateBirthdateCallbackData,
    ProfileUpdateCallbackData,
    ProfileUpdateNameCallbackData,
    ProfileUpdateSurnameCallbackData,
)
from src.bot.profile.finite_state.profile_update_states import ProfileUpdateStates
from src.bot.profile.resources.inline_buttons import (
    get_back_button,
    profile_buttons,
    profile_update_choice_buttons,
)
from src.bot.profile.resources.templates import (
    ASK_NEW_BIRTHDATE_TEMPLATE,
    ASK_NEW_NAME_TEMPLATE,
    ASK_NEW_SURNAME_TEMPLATE,
    WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
    profile_info,
)
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.modules.student_management.domain.enums import Role
from src.modules.student_management.domain.models import Student

__all__ = [
    "include_profile_menu_router",
]


profile_menu_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT,
)


def include_profile_menu_router(root_router: RootRouter) -> None:
    root_router.include_router(profile_menu_router)


@profile_menu_router.callback_query(ProfileUpdateCallbackData.filter())
async def profile_update(callback: CallbackQuery, state: ProfileUpdateContext) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        WHAT_DO_YOU_WANNA_EDIT_TEMPLATE,
        profile_update_choice_buttons(),
    )

    await state.clear()


@profile_menu_router.callback_query(GetBackToProfileCallbackData.filter())
async def back_to_profile(
    callback: CallbackQuery,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
) -> None:
    if callback.message is None:
        return

    edu_info = await get_edu_profile_info_query.execute(student.group_id)

    await safe_message_edit(
        callback,
        profile_info(student, edu_info),
        reply_markup=profile_buttons(),
    )


@profile_menu_router.callback_query(ProfileUpdateNameCallbackData.filter())
async def profile_update_first_name(
    callback: CallbackQuery,
    state: ProfileUpdateContext,
) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        ASK_NEW_NAME_TEMPLATE,
        reply_markup=get_back_button(),
    )
    await state.set_state(ProfileUpdateStates.waiting_new_first_name)


@profile_menu_router.callback_query(ProfileUpdateSurnameCallbackData.filter())
async def profile_update_last_name(
    callback: CallbackQuery,
    state: ProfileUpdateContext,
) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        ASK_NEW_SURNAME_TEMPLATE,
        reply_markup=get_back_button(),
    )
    await state.set_state(ProfileUpdateStates.waiting_new_last_name)


@profile_menu_router.callback_query(ProfileUpdateBirthdateCallbackData.filter())
async def profile_update_birthdate(
    callback: CallbackQuery,
    state: ProfileUpdateContext,
) -> None:
    if callback.message is None:
        return

    await safe_message_edit(
        callback,
        ASK_NEW_BIRTHDATE_TEMPLATE,
        reply_markup=get_back_button(),
    )
    await state.set_state(ProfileUpdateStates.waiting_new_birthdate)
