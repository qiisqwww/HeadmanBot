from aiogram.types import CallbackQuery

from src.bot.profile.callback_data import AskUpdatedFieldValidityCallbackData
from src.bot.common.contextes import ProfileUpdateContext
from src.modules.student_management.domain.models import Student
from src.modules.student_management.domain.enums import ProfileField, Role
from src.bot.profile.profile_update_states import ProfileUpdateStates
from src.bot.common import RootRouter, Router
from src.modules.student_management.application.commands import EditProfileFieldByNameCommand
from src.modules.student_management.application.queries import GetEduProfileInfoQuery
from src.bot.profile.resources.templates import (
    ASK_NEW_NAME_TEMPLATE,
    ASK_NEW_SURNAME_TEMPLATE,
    profile_info
)
from src.bot.profile.resources.inline_buttons import profile_buttons
from src.bot.common.resources.main_menu import main_menu
from src.bot.common.resources.void_inline_buttons import void_inline_buttons
from src.bot.common.resources.templates import your_choice_is_template

__all__ = [
    "include_ask_updated_field_validity_router"
]


ask_updated_field_validity_router = Router(
    must_be_registered=True,
    minimum_role=Role.STUDENT
)


def include_ask_updated_field_validity_router(root_router: RootRouter) -> None:
    root_router.include_router(ask_updated_field_validity_router)


@ask_updated_field_validity_router.callback_query(AskUpdatedFieldValidityCallbackData.filter())
async def ask_new_fullname_validity_callback(
    callback: CallbackQuery,
    callback_data: AskUpdatedFieldValidityCallbackData,
    state: ProfileUpdateContext,
    student: Student,
    get_edu_profile_info_query: GetEduProfileInfoQuery,
    edit_profile_field_by_name_command: EditProfileFieldByNameCommand
) -> None:
    if callback.message is None:
        return

    if callback.message.from_user is None:
        return

    await callback.message.edit_text(
        your_choice_is_template(callback_data.is_field_correct),
        reply_markup=void_inline_buttons(),
    )

    if not callback_data.is_field_correct:
        if callback_data.field_type == ProfileField.NAME:
            await callback.message.answer(
                text=ASK_NEW_NAME_TEMPLATE,
                reply_markup=main_menu(student.role)
            )
            await state.set_state(ProfileUpdateStates.waiting_new_name)
            return
        else:
            await callback.message.answer(
                text=ASK_NEW_SURNAME_TEMPLATE,
                reply_markup=main_menu(student.role)
            )
            await state.set_state(ProfileUpdateStates.waiting_new_surname)
            return

    new_data = await state.new_data
    await edit_profile_field_by_name_command.execute(callback_data.field_type, new_data, student.id)

    if callback_data.is_field_correct:
        edu_info = await get_edu_profile_info_query.execute(student.group_id)
        await callback.message.answer(text=profile_info(student, edu_info), reply_markup=profile_buttons())

    await state.clear()
